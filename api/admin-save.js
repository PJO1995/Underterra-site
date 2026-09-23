const { isAuthorized } = require('./_auth');

const GH_REPO = 'PJO1995/Underterra-site';
const ALLOWED_FILES = {
  inventory: 'admin-inventory.json',
  sold: 'sold.json',
  prices: 'prices.json'
};

const MAX_ATTEMPTS = 4;

function sleep(ms) {
  return new Promise(function (resolve) { setTimeout(resolve, ms); });
}

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

  const url = 'https://api.github.com/repos/' + GH_REPO + '/contents/' + ghFile;
  const contentB64 = Buffer.from(JSON.stringify(data, null, 2) + '\n', 'utf-8').toString('base64');

  try {
    let lastErrText = '';
    for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
      /* Always read the CURRENT sha right before writing -- this is what lets us
         recover from a conflict: another save (or a retry) may have changed the
         file a moment ago, so we re-check instead of trusting a sha we read earlier. */
      const getRes = await fetch(url, {
        headers: { 'Authorization': 'token ' + token, 'Accept': 'application/vnd.github.v3+json' }
      });
      const sha = getRes.ok ? (await getRes.json()).sha : undefined;

      const putBody = {
        message: 'Update ' + ghFile + ' via admin panel',
        content: contentB64
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

      if (putRes.ok) {
        return res.status(200).json({ ok: true, attempts: attempt });
      }

      const errText = await putRes.text();
      lastErrText = errText;
      const isConflict = putRes.status === 409;

      if (!isConflict || attempt === MAX_ATTEMPTS) {
        console.error('GitHub push failed (attempt ' + attempt + '/' + MAX_ATTEMPTS + '):', errText);
        return res.status(502).json({ error: 'GitHub push failed' });
      }

      /* Someone else wrote to this same file a moment before us -- wait a short,
         randomized beat (so two colliding requests don't just collide again on
         the exact same schedule) and retry with a freshly-read sha. */
      console.warn('GitHub write conflict on ' + ghFile + ', retrying (attempt ' + attempt + '/' + MAX_ATTEMPTS + ')');
      await sleep(150 + Math.floor(Math.random() * 300));
    }

    console.error('GitHub push failed after ' + MAX_ATTEMPTS + ' attempts:', lastErrText);
    return res.status(502).json({ error: 'GitHub push failed' });
  } catch (err) {
    console.error('admin-save error:', err);
    return res.status(500).json({ error: 'Server error' });
  }
};
