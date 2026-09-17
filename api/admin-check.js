const { isAuthorized } = require('./_auth');

module.exports = async function handler(req, res) {
  const secret = process.env.SESSION_SECRET;
  const ok = !!secret && isAuthorized(req, secret);
  return res.status(ok ? 200 : 401).json({ ok: ok });
};
