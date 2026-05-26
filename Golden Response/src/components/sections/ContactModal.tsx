"use client";

import React, { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { CyberButton } from "../ui/CyberButton";
import { AlertCircle, CheckCircle, Send, X } from "lucide-react";
import { useReducedMotion } from "@/hooks/useReducedMotion";

interface ContactModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const ContactModal: React.FC<ContactModalProps> = ({ isOpen, onClose }) => {
  const modalRef = useRef<HTMLDivElement>(null);
  const firstInputRef = useRef<HTMLInputElement>(null);
  const shouldReduce = useReducedMotion();

  const [formData, setFormData] = useState({ fullName: "", email: "", phone: "", message: "" });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");

  // Prevent background scroll when modal is active
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
      // Delay focus slightly to allow entrance animation to finish
      const timer = setTimeout(() => {
        firstInputRef.current?.focus();
      }, 150);
      return () => clearTimeout(timer);
    } else {
      document.body.style.overflow = "";
    }
  }, [isOpen]);

  // Handle keys (Escape & Tab Focus Lock for accessibility)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!isOpen) return;

      if (e.key === "Escape") {
        onClose();
        return;
      }

      if (e.key === "Tab") {
        if (!modalRef.current) return;
        const focusable = modalRef.current.querySelectorAll<HTMLElement>(
          'a[href], button:not([disabled]), input:not([disabled]), textarea:not([disabled]), [tabindex="0"]'
        );
        if (focusable.length === 0) return;
        const first = focusable[0];
        const last = focusable[focusable.length - 1];

        if (e.shiftKey) {
          if (document.activeElement === first) {
            last.focus();
            e.preventDefault();
          }
        } else {
          if (document.activeElement === last) {
            first.focus();
            e.preventDefault();
          }
        }
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  // Real-time validations
  const validateField = (name: string, value: string) => {
    let err = "";
    if (name === "fullName") {
      if (!value.trim()) err = "REQUIRED_IDENTITY_FIELD";
    } else if (name === "email") {
      if (!value.trim()) {
        err = "REQUIRED_COMMS_ADDRESS";
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
        err = "INVALID_COMMS_ADDRESS_PATTERN";
      }
    } else if (name === "phone") {
      if (value.trim() && !/^\+?[1-9]\d{1,14}$/.test(value.trim())) {
        err = "INVALID_ITU_PHONE_FORMAT";
      }
    } else if (name === "message") {
      if (!value.trim()) {
        err = "REQUIRED_MESSAGE_BODY";
      } else if (value.trim().length < 10) {
        err = "PAYLOAD_TOO_SHORT_MIN_10";
      }
    }
    return err;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (touched[name]) {
      const err = validateField(name, value);
      setErrors((prev) => ({ ...prev, [name]: err }));
    }
  };

  const handleBlur = (e: React.FocusEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setTouched((prev) => ({ ...prev, [name]: true }));
    const err = validateField(name, value);
    setErrors((prev) => ({ ...prev, [name]: err }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Force validation on all fields
    const newErrors: Record<string, string> = {};
    Object.keys(formData).forEach((key) => {
      const val = formData[key as keyof typeof formData];
      const err = validateField(key, val);
      if (err) newErrors[key] = err;
    });

    setTouched({ fullName: true, email: true, phone: true, message: true });
    setErrors(newErrors);

    if (Object.values(newErrors).some((err) => err)) {
      return;
    }

    setStatus("loading");

    try {
      const res = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (res.ok) {
        setStatus("success");
        setFormData({ fullName: "", email: "", phone: "", message: "" });
        setErrors({});
        setTouched({});
      } else {
        setStatus("error");
      }
    } catch {
      setStatus("error");
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          {/* Backdrop Blur overlay */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="absolute inset-0 bg-cyber-bg/85 backdrop-blur-md"
          />

          {/* Modal window element */}
          <motion.div
            ref={modalRef}
            tabIndex={-1}
            role="dialog"
            aria-modal="true"
            aria-labelledby="modal-title"
            initial={shouldReduce ? { opacity: 0 } : { opacity: 0, scale: 0.95, y: 25 }}
            animate={shouldReduce ? { opacity: 1 } : { opacity: 1, scale: 1, y: 0 }}
            exit={shouldReduce ? { opacity: 0 } : { opacity: 0, scale: 0.95, y: 25 }}
            transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] as const }}
            className="relative w-full max-w-lg bg-cyber-darker border border-cyber-cyan p-8 text-white focus:outline-none overflow-y-auto max-h-[90vh]"
            style={{
              clipPath: "polygon(0 0, 100% 0, 100% calc(100% - 20px), calc(100% - 20px) 100%, 0 100%)",
            }}
          >
            {/* Close toggle */}
            <button
              onClick={onClose}
              className="absolute top-4 right-4 text-gray-500 hover:text-cyber-pink transition-colors focus:outline-none focus-visible:ring-1 focus-visible:ring-cyber-cyan"
              aria-label="Close contact modal"
            >
              <X className="w-5 h-5" />
            </button>

            <h2 id="modal-title" className="text-xl md:text-2xl font-mono text-cyber-cyan tracking-widest mb-6 uppercase">
              // SECURE_COMMS_CHANNEL
            </h2>

            {status === "success" ? (
              <motion.div
                initial={shouldReduce ? { opacity: 0 } : { opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-center py-10"
              >
                <CheckCircle className="w-16 h-16 text-cyber-cyan mx-auto mb-6" />
                <p className="text-cyber-pink font-mono text-base md:text-lg mb-2 uppercase tracking-widest">
                  DATA_TRANSMISSION_SUCCESSFUL
                </p>
                <p className="text-gray-400 text-xs md:text-sm mb-8 leading-relaxed max-w-sm mx-auto">
                  Telemetry handshake complete. Connection node secured. The developer has been alerted via SMTP.
                </p>
                <CyberButton variant="cyan" onClick={() => { setStatus("idle"); onClose(); }} className="w-full">
                  DISCONNECT_COMMS
                </CyberButton>
              </motion.div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-5">
                {status === "error" && (
                  <motion.div
                    initial={{ opacity: 0, y: -5 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="p-3 bg-cyber-pink/15 border border-cyber-pink text-cyber-pink font-mono text-xs flex items-center gap-2"
                  >
                    <AlertCircle className="w-4 h-4 flex-shrink-0" />
                    <span>TRANSMISSION_ERROR: GATEWAY_SERVER_UNRESPONSIVE</span>
                  </motion.div>
                )}

                <div>
                  <label className="block font-mono text-[10px] text-gray-400 mb-1.5 tracking-wider" htmlFor="fullName">
                    FULL_NAME *
                  </label>
                  <input
                    ref={firstInputRef}
                    id="fullName"
                    name="fullName"
                    type="text"
                    required
                    className={`w-full bg-cyber-bg border ${
                      errors.fullName ? "border-cyber-pink" : "border-gray-800 focus:border-cyber-cyan"
                    } p-3 font-mono text-xs text-white outline-none transition-colors duration-200`}
                    value={formData.fullName}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    aria-invalid={!!errors.fullName}
                    aria-describedby={errors.fullName ? "fullName-error" : undefined}
                  />
                  {errors.fullName && (
                    <p id="fullName-error" className="text-cyber-pink font-mono text-[10px] mt-1 flex items-center gap-1">
                      <AlertCircle className="w-3 h-3" /> {errors.fullName}
                    </p>
                  )}
                </div>

                <div>
                  <label className="block font-mono text-[10px] text-gray-400 mb-1.5 tracking-wider" htmlFor="email">
                    EMAIL_ADDRESS *
                  </label>
                  <input
                    id="email"
                    name="email"
                    type="email"
                    required
                    className={`w-full bg-cyber-bg border ${
                      errors.email ? "border-cyber-pink" : "border-gray-800 focus:border-cyber-cyan"
                    } p-3 font-mono text-xs text-white outline-none transition-colors duration-200`}
                    value={formData.email}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    aria-invalid={!!errors.email}
                    aria-describedby={errors.email ? "email-error" : undefined}
                  />
                  {errors.email && (
                    <p id="email-error" className="text-cyber-pink font-mono text-[10px] mt-1 flex items-center gap-1">
                      <AlertCircle className="w-3 h-3" /> {errors.email}
                    </p>
                  )}
                </div>

                <div>
                  <label className="block font-mono text-[10px] text-gray-400 mb-1.5 tracking-wider" htmlFor="phone">
                    COMMS_PHONE (OPTIONAL)
                  </label>
                  <input
                    id="phone"
                    name="phone"
                    type="tel"
                    placeholder="+1234567890"
                    className={`w-full bg-cyber-bg border ${
                      errors.phone ? "border-cyber-pink" : "border-gray-800 focus:border-cyber-cyan"
                    } p-3 font-mono text-xs text-white outline-none transition-colors duration-200`}
                    value={formData.phone}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    aria-invalid={!!errors.phone}
                    aria-describedby={errors.phone ? "phone-error" : undefined}
                  />
                  {errors.phone && (
                    <p id="phone-error" className="text-cyber-pink font-mono text-[10px] mt-1 flex items-center gap-1">
                      <AlertCircle className="w-3 h-3" /> {errors.phone}
                    </p>
                  )}
                </div>

                <div>
                  <label className="block font-mono text-[10px] text-gray-400 mb-1.5 tracking-wider" htmlFor="message">
                    PAYLOAD_MESSAGE_BODY *
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    required
                    rows={4}
                    className={`w-full bg-cyber-bg border ${
                      errors.message ? "border-cyber-pink" : "border-gray-800 focus:border-cyber-cyan"
                    } p-3 font-mono text-xs text-white outline-none transition-colors duration-200 resize-none`}
                    value={formData.message}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    aria-invalid={!!errors.message}
                    aria-describedby={errors.message ? "message-error" : undefined}
                  />
                  {errors.message && (
                    <p id="message-error" className="text-cyber-pink font-mono text-[10px] mt-1 flex items-center gap-1">
                      <AlertCircle className="w-3 h-3" /> {errors.message}
                    </p>
                  )}
                </div>

                <div className="flex gap-4 pt-3">
                  <CyberButton type="submit" variant="cyan" disabled={status === "loading"} className="flex-1">
                    <span className="flex items-center gap-2">
                      <Send className="w-4.5 h-4.5" />
                      {status === "loading" ? "TRANSMITTING..." : "BROADCAST_PAYLOAD"}
                    </span>
                  </CyberButton>
                  
                  <CyberButton
                    type="button"
                    variant="purple"
                    onClick={onClose}
                    disabled={status === "loading"}
                  >
                    ABORT
                  </CyberButton>
                </div>
              </form>
            )}
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};
export default ContactModal;
