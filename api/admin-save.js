const { isAuthorized } = require('./_auth');

const GH_REPO = 'PJO1995/Underterra-site';
const ALLOWED_FILES = {
  inventory: 'admin-inventory.json',
  sold: 'sold.json',
  prices: 'prices.json'
};

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const secret = process.env.SESSION_SECRET;
  if (!secret || !isAuthorized(req, secret)) return res.status(401).json({ error: 'Unauthorized' });

  const token = process.env.GH_TOKEN;
  if (!token) return res.status(500).json({ error: 'Server not configured. Missing GH_TOKEN.' });

  const body = req.body || {};
  const file = body.file;
  const data = body.data;
  const ghFile = ALLOWED_FILES[file];
  if (!ghFile || data === undefined) {
    return res.status(400).json({ error: 'Invalid request' });
  }

  try {
    const url = 'https://api.github.com/repos/' + GH_REPO + '/contents/' + ghFile;
    const getRes = await fetch(url, {
      headers: { 'Authorization': 'token ' + token, 'Accept': 'application/vnd.github.v3+json' }
    });
    const sha = getRes.ok ? (await getRes.json()).sha : undefined;

    const putBody = {
      message: 'Update ' + ghFile + ' via admin panel',
      content: Buffer.from(JSON.stringify(data, null, 2) + '\n', 'utf-8').toString('base64')
    };
    if (sha) putBody.sha = sha;

    const putRes = await fetch(url, {
      method: 'PUT',
      headers: {
        'Authorization': 'token ' + token,
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(putBody)
    });

    if (!putRes.ok) {
      const errText = await putRes.text();
      console.error('GitHub push failed:', errText);
      return res.status(502).json({ error: 'GitHub push failed' });
    }
    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('admin-save error:', err);
    return res.status(500).json({ error: 'Server error' });
  }
};
