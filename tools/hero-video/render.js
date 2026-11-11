/* scene.html 을 프레임으로 렌더링해 ffmpeg 로 인코딩한다.
   사용: NODE_PATH=<playwright-core 위치> CHROME_PATH=<크롬> FFMPEG=<ffmpeg> node tools/hero-video/render.js <출력폴더>
   결과: <출력폴더>/hero.mp4, hero-poster.jpg */
const path = require('path');
const fs = require('fs');
const { spawnSync } = require('child_process');
const { chromium } = require('playwright-core');

const SECONDS = 10;
const FPS = 24;
const out = process.argv[2];
if (!out) throw new Error('출력 폴더를 지정하세요');
const frames = path.join(out, 'frames');
fs.mkdirSync(frames, { recursive: true });

(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.join(__dirname, 'scene.html'));
  const total = SECONDS * FPS;
  for (let i = 0; i < total; i++) {
    await page.evaluate((t) => window.render(t), i / total);
    await page.locator('#c').screenshot({ path: path.join(frames, String(i).padStart(4, '0') + '.png') });
  }
  await browser.close();

  const run = (args) => {
    const r = spawnSync(process.env.FFMPEG, args, { encoding: 'utf8' });
    if (r.status !== 0) throw new Error(r.stderr.slice(-800));
  };
  run(['-y', '-framerate', String(FPS), '-i', path.join(frames, '%04d.png'),
    '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-crf', '24',
    '-preset', 'slow', '-movflags', '+faststart', '-an', path.join(out, 'hero.mp4')]);
  run(['-y', '-i', path.join(frames, '0000.png'), '-q:v', '4', path.join(out, 'hero-poster.jpg')]);
  console.log('done', fs.statSync(path.join(out, 'hero.mp4')).size);
})();
