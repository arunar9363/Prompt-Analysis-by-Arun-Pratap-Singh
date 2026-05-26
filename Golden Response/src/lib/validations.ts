import validator from "validator";

export interface CleanContactInput {
  fullName: string;
  email: string;
  phone?: string;
  message: string;
}

export function sanitizeAndValidateContact(body: any): CleanContactInput {
  if (!body || typeof body !== "object") {
    throw new Error("Malformed JSON payload mapping context.");
  }

  let { fullName, email, phone, message } = body;

  // Enforce types and clean values to prevent XSS and schema contamination
  fullName = typeof fullName === "string" ? validator.escape(fullName.trim()) : "";
  const rawEmail = typeof email === "string" ? email.trim() : "";
  phone = typeof phone === "string" ? validator.escape(phone.trim()) : "";
  message = typeof message === "string" ? validator.escape(message.trim()) : "";

  // Perform validations
  if (validator.isEmpty(fullName)) {
    throw new Error("Field validation error: fullName required.");
  }
  if (validator.isEmpty(rawEmail) || !validator.isEmail(rawEmail)) {
    throw new Error("Field validation error: valid email context required.");
  }
  
  // Normalize the validated email safely
  const normalizedEmail = validator.normalizeEmail(rawEmail);
  if (!normalizedEmail) {
    throw new Error("Field validation error: valid email normalization failure.");
  }
  email = normalizedEmail;

  if (!validator.isEmpty(phone)) {
    // Basic mobile phone validation (allows leading +, and common characters)
    if (!validator.isMobilePhone(phone, "any")) {
      throw new Error("Field validation error: Invalid phone sequencing profile.");
    }
  }

  if (validator.isEmpty(message) || !validator.isLength(message, { min: 10, max: 2000 })) {
    throw new Error("Field validation error: Message length constraint failure (must be 10 - 2000 characters).");
  }

  return { fullName, email, phone: phone || undefined, message };
}
