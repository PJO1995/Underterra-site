const crypto = require('crypto');

const COOKIE_NAME = 'admin_session';

function sign(payload, secret) {
  return crypto.createHmac('sha256', secret).update(payload).digest('hex');
}

function safeEqual(a, b) {
  const ab = Buffer.from(String(a));
  const bb = Buffer.from(String(b));
  if (ab.length !== bb.length) return false;
  return crypto.timingSafeEqual(ab, bb);
}

function createSessionCookie(secret, ttlMs) {
  const exp = Date.now() + ttlMs;
  const payload = String(exp);
  const sig = sign(payload, secret);
  const value = payload + '.' + sig;
  const maxAge = Math.floor(ttlMs / 1000);
  return COOKIE_NAME + '=' + value + '; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=' + maxAge;
}

function clearSessionCookie() {
  return COOKIE_NAME + '=; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=0';
}

function isAuthorized(req, secret) {
  const cookieHeader = req.headers.cookie || '';
  const parts = cookieHeader.split(';').map(function (s) { return s.trim(); });
  const found = parts.find(function (s) { return s.indexOf(COOKIE_NAME + '=') === 0; });
  if (!found) return false;
  const value = found.slice((COOKIE_NAME + '=').length);
  const segs = value.split('.');
  if (segs.length !== 2) return false;
  const payload = segs[0];
  const sig = segs[1];
  const expected = sign(payload, secret);
  if (!safeEqual(sig, expected)) return false;
  const exp = parseInt(payload, 10);
  if (!exp || Date.now() > exp) return false;
  return true;
}

module.exports = { createSessionCookie, clearSessionCookie, isAuthorized, safeEqual };
