"""Shared attribution for this project's public HTML packages."""
import re

DESIGN_CREDIT_HTML='<p id="design-attribution" style="font-size:13px;line-height:1.6;color:#53606b">Design by <strong>CL Kao</strong> · Powered by <a href="https://spacedock.md/" target="_blank" rel="noopener">spacedock.md</a></p>'

def add_attribution(source):
    if 'id="design-attribution"'in source:return source
    if '<aside'in source:
        return re.sub(r'(<aside[^>]*>)',lambda m:m[0]+DESIGN_CREDIT_HTML,source,count=1)
    if '</footer>'in source:return source.replace('</footer>',DESIGN_CREDIT_HTML+'</footer>',1)
    if '</body>'in source:return source.replace('</body>','<footer>'+DESIGN_CREDIT_HTML+'</footer></body>',1)
    if '<script'in source:return source.replace('<script','<footer>'+DESIGN_CREDIT_HTML+'</footer><script',1)
    return source+'<footer>'+DESIGN_CREDIT_HTML+'</footer>'
