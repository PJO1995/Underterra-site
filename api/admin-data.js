const { isAuthorized } = require('./_auth');

const GH_REPO = 'PJO1995/Underterra-site';
const GH_FILE = 'admin-inventory.json';

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  const secret = process.env.SESSION_SECRET;
  if (!secret || !isAuthorized(req, secret)) return res.status(401).json({ error: 'Unauthorized' });

  const token = process.env.GH_TOKEN;
  if (!token) return res.status(500).json({ error: 'Server not configured. Missing GH_TOKEN.' });

  try {
    const url = 'https://api.github.com/repos/' + GH_REPO + '/contents/' + GH_FILE;
    const ghRes = await fetch(url, {
      headers: { 'Authorization': 'token ' + token, 'Accept': 'application/vnd.github.v3+json' }
    });
    if (ghRes.status === 404) {
      return res.status(200).json({ lastUpdated: null, inventory: [] });
    }
    if (!ghRes.ok) {
      return res.status(502).json({ error: 'GitHub read failed' });
    }
    const fileData = await ghRes.json();
    const content = Buffer.from(fileData.content, 'base64').toString('utf-8');
    const parsed = JSON.parse(content);
    return res.status(200).json(parsed);
  } catch (err) {
    console.error('admin-data error:', err);
    return res.status(500).json({ error: 'Server error' });
  }
};
