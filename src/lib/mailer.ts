import nodemailer from "nodemailer";

export interface MailPayload {
  fullName: string;
  email: string;
  phone?: string;
  message: string;
}

export async function sendNotificationEmail(payload: MailPayload) {
  const host = process.env.SMTP_HOST;
  const port = Number(process.env.SMTP_PORT) || 587;
  const user = process.env.SMTP_USER;
  const pass = process.env.SMTP_PASSWORD;
  const toEmail = process.env.CONTACT_NOTIFICATION_EMAIL || "developer@cyberdomain.tech";

  const emailText = `Telemetry Inbound\n\nIdentity: ${payload.fullName}\nComms: ${payload.email}\nPhone: ${payload.phone || "NONE"}\nPayload:\n${payload.message}\nTimestamp: ${new Date().toISOString()}`;
  
  const emailHtml = `
    <div style="background:#05050a; color:#ffffff; padding:25px; font-family:monospace; border:2px solid #00f0ff; max-width: 600px; margin: auto;">
      <h2 style="color:#00f0ff; border-bottom:2px solid #00f0ff; padding-bottom:10px; margin-top:0;">[COMMS_ALERT] INBOUND HANDSHAKE</h2>
      <p style="margin: 10px 0;"><strong>IDENTITY:</strong> ${payload.fullName}</p>
      <p style="margin: 10px 0;"><strong>COMMS LINK:</strong> <a href="mailto:${payload.email}" style="color: #00f0ff; text-decoration: none;">${payload.email}</a></p>
      <p style="margin: 10px 0;"><strong>ITU PHONE:</strong> ${payload.phone || "NOT_PROVIDED"}</p>
      <p style="margin: 10px 0; color: #888;"><strong>TIMESTAMP:</strong> ${new Date().toISOString()}</p>
      <div style="background:#121224; padding:20px; border-left:4px solid #ff007f; margin-top:20px; border-radius: 4px;">
        <strong style="color: #ff007f;">DATA_PAYLOAD:</strong><br/>
        <p style="white-space: pre-wrap; font-family: inherit; color: #e2e8f0; margin-top: 10px; line-height: 1.6;">${payload.message}</p>
      </div>
    </div>
  `;

  // Fallback check: log message if SMTP credentials are missing or default placeholders
  const isDummyHost = !host || (host.includes("sendgrid.net") && user === "apikey" && pass?.includes("production_secure_key_here"));
  if (isDummyHost || !host || !user || !pass) {
    console.warn(
      "[MAILER WARNING] SMTP credentials are not configured or are placeholder keys in .env.local.\n" +
      "Skipping live SMTP delivery to prevent client timeout. Logging payload below instead:"
    );
    console.log("\n=================== LOCAL TELEMETRY MOCK LOG ===================");
    console.log(emailText);
    console.log("==============================================================\n");
    return { success: true, mode: "log_fallback" };
  }

  // Create transporter
  const transporter = nodemailer.createTransport({
    host,
    port,
    secure: port === 465, // True for 465, false for 587/25
    auth: {
      user,
      pass,
    },
  });

  const mailOptions = {
    from: `"Cyber Portfolio Alert" <${toEmail}>`,
    to: toEmail,
    subject: `[COMMS_ALERT] Handshake Node: ${payload.fullName}`,
    text: emailText,
    html: emailHtml,
  };

  // Implement resilient 3-attempt retry loop
  let attempt = 0;
  const maxAttempts = 3;
  while (attempt < maxAttempts) {
    try {
      console.log(`[MAILER] Initiating SMTP relay... (Attempt ${attempt + 1}/${maxAttempts})`);
      await transporter.sendMail(mailOptions);
      console.log("[MAILER] SMTP transmission accomplished successfully!");
      return { success: true, mode: "smtp" };
    } catch (err: any) {
      attempt++;
      console.error(`[MAILER ERROR] Failed during SMTP dispatch on attempt ${attempt}:`, err.message || err);
      if (attempt >= maxAttempts) {
        throw new Error(`SMTP relay dispatch completely failed after ${maxAttempts} retries. details: ${err.message}`);
      }
    }
  }

  return { success: false, mode: "failed" };
}
