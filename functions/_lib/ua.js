// Leitura de user agent no servidor. Sem biblioteca externa: o objetivo é
// classificar (navegador, SO, tipo de dispositivo, bot), não identificar versão exata.

const BOTS = /bot|crawl|spider|slurp|bingpreview|facebookexternalhit|whatsapp|telegram|discord|slack|preview|monitor|pingdom|uptime|headless|lighthouse|gtmetrix|curl|wget|python-requests|axios|node-fetch|postman|semrush|ahrefs|mj12|dotbot|petal|yandex|baidu|duckduck|applebot|amazonbot|gptbot|claudebot|perplexity|ccbot|bytespider/i;

export function lerUA(ua = '') {
  const s = String(ua);
  const is_bot = BOTS.test(s) || s.trim() === '';

  let navegador = 'Outro';
  if (/edg\//i.test(s)) navegador = 'Edge';
  else if (/opr\/|opera/i.test(s)) navegador = 'Opera';
  else if (/samsungbrowser/i.test(s)) navegador = 'Samsung Internet';
  else if (/chrome|crios/i.test(s)) navegador = 'Chrome';
  else if (/firefox|fxios/i.test(s)) navegador = 'Firefox';
  else if (/safari/i.test(s)) navegador = 'Safari';
  if (is_bot) navegador = 'Bot';

  let so = 'Outro';
  if (/windows nt/i.test(s)) so = 'Windows';
  else if (/android/i.test(s)) so = 'Android';
  else if (/iphone|ipad|ipod/i.test(s)) so = 'iOS';
  else if (/mac os x|macintosh/i.test(s)) so = 'macOS';
  else if (/linux/i.test(s)) so = 'Linux';

  let dispositivo = 'desktop';
  if (is_bot) dispositivo = 'bot';
  else if (/ipad|tablet|playbook|silk|(android(?!.*mobile))/i.test(s)) dispositivo = 'tablet';
  else if (/mobi|iphone|ipod|android.*mobile|windows phone/i.test(s)) dispositivo = 'mobile';

  return { navegador, so, dispositivo, is_bot };
}
