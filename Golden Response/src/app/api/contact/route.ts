import { NextRequest, NextResponse } from "next/server";
import { connectToDatabase, Contact } from "@/lib/db";
import { sanitizeAndValidateContact } from "@/lib/validations";
import { sendNotificationEmail } from "@/lib/mailer";

// In-memory rate limiting map (IP based)
const rateLimitMap = new Map<string, { count: number; resetTime: number }>();

function checkRateLimit(ip: string): boolean {
  const now = Date.now();
  const limitWindow = 60 * 1000; // 1 Minute Window
  const maxRequests = 3;

  const clientData = rateLimitMap.get(ip);
  if (!clientData) {
    rateLimitMap.set(ip, { count: 1, resetTime: now + limitWindow });
    return true;
  }

  if (now > clientData.resetTime) {
    rateLimitMap.set(ip, { count: 1, resetTime: now + limitWindow });
    return true;
  }

  if (clientData.count >= maxRequests) {
    return false;
  }

  clientData.count++;
  return true;
}

export async function POST(req: NextRequest) {
  // Extract tracking IP address safely
  const ip = req.headers.get("x-forwarded-for") || "127.0.0.1";
  const userAgent = req.headers.get("user-agent") || "UNKNOWN";

  // Rate limiter check
  if (!checkRateLimit(ip)) {
    console.warn(`[SECURITY] Throttled request from IP: ${ip}`);
    return new NextResponse(
      JSON.stringify({ 
        error: "TOO_MANY_REQUESTS", 
        message: "Comms transmission rate limit breached. Please retry in 60s." 
      }),
      { 
        status: 429, 
        headers: { 
          "Content-Type": "application/json",
          "X-Content-Type-Options": "nosniff",
          "X-Frame-Options": "DENY"
        } 
      }
    );
  }

  try {
    const jsonBody = await req.json();
    
    // Validate and Sanitize payload to prevent injection exploits
    const cleanData = sanitizeAndValidateContact(jsonBody);

    // Save record to MongoDB via Mongoose model
    await connectToDatabase();
    const contactRecord = new Contact({
      fullName: cleanData.fullName,
      email: cleanData.email,
      phone: cleanData.phone,
      message: cleanData.message,
      ipAddress: ip,
      userAgent: userAgent,
    });
    await contactRecord.save();
    console.log(`[DATABASE] Successfully persisted contact record from ${cleanData.fullName}`);

    // Trigger SMTP email alert to developer
    await sendNotificationEmail(cleanData);

    return new NextResponse(
      JSON.stringify({ status: "TRANSMITTED", recipient: cleanData.email }),
      { 
        status: 200, 
        headers: { 
          "Content-Type": "application/json",
          "X-Content-Type-Options": "nosniff",
          "X-Frame-Options": "DENY"
        } 
      }
    );

  } catch (error: any) {
    console.error(`[API ERROR] Failure in contact gateway:`, error.message || error);
    return new NextResponse(
      JSON.stringify({ error: "TRANSMISSION_FAILURE", details: error.message }),
      { 
        status: 400, 
        headers: { 
          "Content-Type": "application/json",
          "X-Content-Type-Options": "nosniff",
          "X-Frame-Options": "DENY"
        } 
      }
    );
  }
}
