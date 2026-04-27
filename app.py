"""
Digital Asset Protection — Flask Backend
"""
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import random, string, hashlib
from datetime import datetime, timedelta

# Serve static HTML files (frontend) from the same directory as this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(BASE_DIR, filename)

def _hex(n=64): return '0x' + ''.join(random.choices('0123456789abcdef', k=n))
def _id(): return f"DAP-{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}"
def _addr(): return '0x' + ''.join(random.choices('0123456789abcdef', k=40))
def _ago(h=720): return (datetime.utcnow() - timedelta(minutes=random.randint(1, h*60))).isoformat() + 'Z'

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat() + 'Z'})

@app.route('/api/stats')
def stats():
    return jsonify({"total_assets":1247,"protected_streams":89,"active_alerts":23,"detection_accuracy":91.4,"watermarks_embedded":3421,"ledger_entries":1247,"takedown_requests":156,"compliance_score":96.8,"assets_monitored_24h":4523,"infringements_blocked":847,"avg_response_time_ms":230,"uptime":99.97})

@app.route('/api/alerts')
def alerts():
    plats=['YouTube','Twitter/X','Facebook','Telegram','Reddit','TikTok','Instagram','Dailymotion']
    sevs=['critical','high','medium','low']
    ctypes=['Live Stream','Highlight Reel','Match Footage','Player Interview','Press Conference']
    sts=['active','investigating','resolved','escalated']
    ds=["Unauthorized redistribution detected","Stream rip identified with watermark match","Modified highlight clip uploaded without license","API scraping pattern detected","Re-encoded footage on unauthorized channel","Clipped content circulating on messaging apps","Geo-blocked content accessed via VPN tunnel"]
    r=[]
    for i in range(20):
        r.append({"id":f"ALT-{1000+i}","timestamp":_ago(48),"platform":random.choice(plats),"severity":random.choice(sevs),"content_type":random.choice(ctypes),"description":random.choice(ds),"status":random.choice(sts),"confidence":round(random.uniform(.75,.99),2),"watermark_match":random.choice([True,True,False])})
    r.sort(key=lambda x:x['timestamp'],reverse=True)
    return jsonify({"alerts":r,"total":len(r)})

@app.route('/api/ledger')
def ledger():
    names=["Premier League Match 38 — Arsenal vs Man City","NBA Finals Game 7 — Full Broadcast","FIFA World Cup QF — Argentina vs Netherlands","UFC 300 Main Event — Full Fight","Wimbledon Final — Djokovic vs Alcaraz","Super Bowl LVIII — Full Coverage","Champions League Final 2024","F1 Monaco GP — Race Footage","NFL Playoffs — Chiefs vs Bills","IPL Final 2024 — Full Match"]
    es=[]
    for i,n in enumerate(names):
        es.append({"tx_hash":_hex(),"block_number":18900000+i*random.randint(100,500),"asset_id":_id(),"asset_name":n,"owner":_addr(),"license_type":random.choice(["exclusive","non-exclusive","territorial","time-limited"]),"territory":random.choice(["global","north-america","europe","asia-pacific","mena"]),"valid_from":(datetime.utcnow()-timedelta(days=random.randint(30,365))).strftime('%Y-%m-%d'),"valid_until":(datetime.utcnow()+timedelta(days=random.randint(30,730))).strftime('%Y-%m-%d'),"status":random.choice(["active","active","active","expired"]),"watermark_id":f"WM-{random.randint(10000,99999)}","timestamp":_ago(720)})
    return jsonify({"entries":es,"total":len(es)})

@app.route('/api/detect', methods=['POST'])
def detect():
    d=request.get_json() or {}
    url=d.get('url','https://example.com/video.mp4')
    inf=random.random()>.25
    c=round(random.uniform(.78,.97),2) if inf else round(random.uniform(.08,.35),2)
    return jsonify({"url_analyzed":url,"is_infringing":inf,"confidence":c,"matched_asset":_id() if inf else None,"watermark_detected":inf and random.random()>.25,"analysis_time_ms":random.randint(120,450),"fingerprint_hash":hashlib.md5(url.encode()).hexdigest() if inf else None,"detection_method":random.choice(["watermark_matching","perceptual_hashing","scene_matching","audio_fingerprinting"]) if inf else None,"recommended_action":"takedown" if c>.9 and inf else "monitor" if inf else "none","timestamp":datetime.utcnow().isoformat()+'Z'})

@app.route('/api/workflow')
def workflow():
    return jsonify({"phases":[{"step":1,"name":"Discovery & Scoping","status":"completed","progress":100,"desc":"Map content pipelines, identify stakeholders, classify asset types."},{"step":2,"name":"Threat Modeling","status":"completed","progress":100,"desc":"Analyze attack vectors — stream ripping, social media piracy, API scraping."},{"step":3,"name":"Watermarking Engine","status":"completed","progress":100,"desc":"Invisible perceptual watermarks via FFmpeg — no quality degradation."},{"step":4,"name":"Blockchain Ledger","status":"completed","progress":100,"desc":"On-chain registry for ownership, licensing, and distribution rights."},{"step":5,"name":"AI Detection Module","status":"active","progress":78,"desc":"ML models on perceptual hashing, scene matching, audio fingerprinting."},{"step":6,"name":"Monitoring Dashboard","status":"active","progress":65,"desc":"Real-time analytics, alerts with confidence scores, takedown tracking."},{"step":7,"name":"Testing & Demo","status":"pending","progress":0,"desc":"Simulate piracy, validate accuracy above 85%, present pipeline."}],"overall_progress":77.6})

@app.route('/api/features')
def features():
    return jsonify({"core":[{"icon":"fa-shield-halved","title":"Real-Time Monitoring","desc":"Continuously scan 50+ streaming platforms and social networks for unauthorized sports content redistribution.","stat":"50+","stat_label":"Platforms"},{"icon":"fa-fingerprint","title":"Invisible Watermarking","desc":"Embed perceptual watermarks into every frame without quality loss. Each distributor receives a unique identifier.","stat":"3,421","stat_label":"Watermarks"},{"icon":"fa-brain","title":"AI Content Detection","desc":"Machine learning models trained on perceptual hashing, scene analysis, and audio fingerprinting.","stat":"91.4%","stat_label":"Accuracy"},{"icon":"fa-cube","title":"Blockchain Provenance","desc":"Immutable on-chain records of ownership, licensing, and distribution rights for every registered asset.","stat":"1,247","stat_label":"On-chain"},{"icon":"fa-bolt","title":"Instant Takedown","desc":"Automated takedown requests generated and dispatched within 230ms of infringement confirmation.","stat":"230ms","stat_label":"Response"},{"icon":"fa-scale-balanced","title":"Compliance Engine","desc":"Built-in compliance with DMCA, EU Digital Single Market directive, and regional frameworks.","stat":"96.8%","stat_label":"Score"}],"advanced":[{"icon":"fa-network-wired","title":"CDN Integration","desc":"REST API connectors for seamless integration with major content delivery networks."},{"icon":"fa-lock","title":"DRM Encryption","desc":"Multi-DRM support including Widevine, FairPlay, and PlayReady."},{"icon":"fa-chart-line","title":"Analytics Suite","desc":"Content performance, geographic distribution, and piracy trend forecasting."},{"icon":"fa-users-gear","title":"Role-Based Access","desc":"Granular permissions for content managers, legal teams, and administrators."},{"icon":"fa-globe","title":"Geo-Fencing","desc":"Territory-based access controls with VPN detection."},{"icon":"fa-code-branch","title":"API-First Design","desc":"RESTful APIs for custom integrations and white-label deployment."}]})
def init_db():
    conn = sqlite3.connect('dap.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS detections
                 (id TEXT, url TEXT, is_infringing INTEGER, 
                  confidence REAL, reason TEXT, matched_asset TEXT,
                  recommended_action TEXT, timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS ledger
                 (id TEXT, asset_name TEXT, hash TEXT, 
                  block_number INTEGER, timestamp TEXT)''')
    conn.commit()
    conn.close()

init_db()  # call this before app.run()
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
