"""Self-contained citation clipboard control; no network or parent-page access."""
import json


def copy_button_html(plain):
    payload=json.dumps(dict(plain=plain),ensure_ascii=True).replace('<','\\u003c')
    return '''<!doctype html><html lang="zh"><meta charset="utf-8">
<style>body{margin:0;font:14px system-ui;color:#253b34}button{padding:7px 14px;
border:1px solid #9baa9f;border-radius:6px;background:#fffdf7;color:#253b34;cursor:pointer}
#status{margin-left:10px}textarea{width:95%;height:55px}</style>
<button id="copy" type="button">复制引用</button><span id="status" role="status"></span>
<textarea id="fallback" aria-label="引用文本，按 Ctrl+C 复制" hidden readonly></textarea>
<script>const payload='''+payload+''';
document.getElementById('copy').addEventListener('click',async()=>{
 const status=document.getElementById('status');
 try {
  await navigator.clipboard.writeText(payload.plain);
  status.textContent='已复制';
 } catch(e) {
  const area=document.getElementById('fallback'); area.hidden=false;
  area.value=payload.plain; area.focus(); area.select();
  status.textContent=document.execCommand('copy')?'已复制':'请选择下方文字，按 Ctrl+C 复制';
 }
});</script></html>'''
