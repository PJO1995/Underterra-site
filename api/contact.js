const nodemailer = require('nodemailer');

module.exports = async function handler(req, res) {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { firstName, lastName, email, phone, equipment, message } = req.body;

  if (!firstName || !email || !message) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  const transporter = nodemailer.createTransport({
    host: 'smtp.office365.com',
    port: 587,
    secure: false,
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASS,
    },
    tls: { ciphers: 'SSLv3' }
  });

  const subject = `[Underterra] Quote Request — ${firstName} ${lastName}`;

  const html = `
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;">
      <div style="background:#1a1a1a;padding:20px;text-align:center;">
        <h2 style="color:#E8970A;margin:0;">UNDERTERRA</h2>
        <p style="color:#aaa;margin:4px 0 0;">New Quote Request from Website</p>
      </div>
      <div style="padding:24px;background:#f9f9f9;">
        <table style="width:100%;border-collapse:collapse;">
          <tr><td style="padding:8px;font-weight:bold;width:140px;">Name:</td>
              <td style="padding:8px;">${firstName} ${lastName}</td></tr>
          <tr style="background:#fff;"><td style="padding:8px;font-weight:bold;">Email:</td>
              <td style="padding:8px;"><a href="mailto:${email}">${email}</a></td></tr>
          <tr><td style="padding:8px;font-weight:bold;">Phone:</td>
              <td style="padding:8px;">${phone || '—'}</td></tr>
          <tr style="background:#fff;"><td style="padding:8px;font-weight:bold;">Equipment:</td>
              <td style="padding:8px;">${equipment || 'Not specified'}</td></tr>
          <tr><td style="padding:8px;font-weight:bold;vertical-align:top;">Message:</td>
              <td style="padding:8px;">${message.replace(/\n/g, '<br>')}</td></tr>
        </table>
      </div>
      <div style="background:#1a1a1a;padding:12px;text-align:center;">
        <p style="color:#666;font-size:12px;margin:0;">underterradelrio.com — Del Rio, TX</p>
      </div>
    </div>
  `;

  const text = `New Quote Request\n\nName: ${firstName} ${lastName}\nEmail: ${email}\nPhone: ${phone || '—'}\nEquipment: ${equipment || 'Not specified'}\nMessage:\n${message}`;

  try {
    await transporter.sendMail({
      from: `"Underterra Website" <${process.env.SMTP_USER}>`,
      to: process.env.SMTP_USER,
      replyTo: email,
      subject,
      html,
      text,
    });
    return res.status(200).json({ success: true });
  } catch (err) {
    console.error('SMTP error:', err);
    return res.status(500).json({ error: 'Failed to send email' });
  }
};
