const { createSessionCookie, safeEqual } = require('./_auth');

const SESSION_TTL_MS = 8 * 60 * 60 * 1000; // 8 hours

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const expected = process.env.ADMIN_PASSWORD;
  const secret = process.env.SESSION_SECRET;
  if (!expected || !secret) {
    return res.status(500).json({ error: 'Server not configured. Missing ADMIN_PASSWORD or SESSION_SECRET.' });
  }

  const body = req.body || {};
  const password = body.password;
  if (typeof password !== 'string' || !safeEqual(password, expected)) {
    return res.status(401).json({ error: 'Incorrect password' });
  }

  res.setHeader('Set-Cookie', createSessionCookie(secret, SESSION_TTL_MS));
  return res.status(200).json({ ok: true });
};
