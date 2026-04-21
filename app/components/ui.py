import streamlit as st


def inject_css():
    st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}

/* ── Hover & transition effects ── */
.mc{border-radius:12px;padding:1.1rem 1.25rem;transition:transform .2s,box-shadow .2s;}
.mc:hover{transform:translateY(-2px);box-shadow:0 4px 14px rgba(255,255,255,.07);}
.mc .v{font-size:1.9rem;font-weight:700;line-height:1;}
.mc .l{font-size:.72rem;font-weight:500;margin-top:4px;text-transform:uppercase;letter-spacing:.06em;opacity:.65;}
.mc.blue .v{color:#60a5fa;} .mc.green .v{color:#34d399;} .mc.red .v{color:#f87171;} .mc.amber .v{color:#fbbf24;}

/* ── Badges ── */
.badge{display:inline-block;padding:3px 10px;border-radius:20px;font-size:.72rem;font-weight:600;letter-spacing:.03em;}
.b-pending{background:#fef3c7;color:#92400e;} .b-assigned{background:#dbeafe;color:#1e40af;}
.b-inprogress{background:#ede9fe;color:#5b21b6;} .b-resolved{background:#d1fae5;color:#065f46;}
.b-closed{background:#f1f5f9;color:#475569;}
.b-low{background:#d1fae5;color:#065f46;} .b-medium{background:#fef3c7;color:#92400e;}
.b-high{background:#fee2e2;color:#991b1b;}
.b-critical{background:#dc2626;color:white;animation:pulse 1.5s infinite;}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.75}}

/* ── Page header ── */
.ph{padding-bottom:.6rem;margin-bottom:1.1rem;border-bottom:2px solid rgba(255,255,255,.1);}
.ph h2{font-weight:700;margin:0;font-size:1.45rem;}
.ph p{opacity:.65;margin:.2rem 0 0;font-size:.875rem;}

/* ── Timeline ── */
.tl-item{display:flex;gap:12px;margin-bottom:.9rem;position:relative;}
.tl-dot{width:12px;height:12px;border-radius:50%;background:#60a5fa;margin-top:4px;flex-shrink:0;box-shadow:0 0 0 2px #60a5fa,0 0 0 4px rgba(96,165,250,.2);}
.tl-dot.res{background:#34d399;box-shadow:0 0 0 2px #34d399,0 0 0 4px rgba(52,211,153,.2);}
.tl-dot.cls{background:#9ca3af;box-shadow:0 0 0 2px #9ca3af;}
.tl-line{position:absolute;left:5px;top:16px;bottom:-8px;width:2px;background:rgba(255,255,255,.1);}
.tl-action{font-weight:600;font-size:.85rem;}
.tl-meta{font-size:.72rem;opacity:.55;margin-top:2px;}
.tl-note{font-size:.8rem;border-radius:6px;padding:5px 10px;margin-top:4px;border-left:3px solid rgba(255,255,255,.15);opacity:.8;}

/* ── Progress tracker ── */
.pt{display:flex;align-items:center;justify-content:space-between;padding:1.25rem 0;position:relative;}
.pt::before{content:'';position:absolute;top:50%;left:5%;right:5%;height:3px;background:rgba(255,255,255,.1);z-index:0;transform:translateY(-8px);}
.pt-step{display:flex;flex-direction:column;align-items:center;gap:6px;z-index:1;}
.pt-circle{width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:.85rem;font-weight:700;border:3px solid rgba(255,255,255,.15);transition:all .35s;opacity:.5;}
.pt-circle.done{background:#34d399;color:white;border-color:#34d399;opacity:1;}
.pt-circle.cur{background:#60a5fa;color:white;border-color:#60a5fa;box-shadow:0 0 0 6px rgba(96,165,250,.2);opacity:1;}
.pt-label{font-size:.68rem;text-align:center;max-width:68px;line-height:1.2;opacity:.5;}
.pt-label.done{color:#34d399;font-weight:600;opacity:1;} .pt-label.cur{color:#60a5fa;font-weight:700;opacity:1;}

/* ── Critical alert ── */
.crit{border:1.5px solid #f87171;border-radius:12px;padding:1rem 1.25rem;margin:.5rem 0;}
.crit h4{color:#f87171;margin:0 0 .4rem;font-size:.95rem;}
.crit a{color:#60a5fa;font-weight:600;}

/* ── Close request banner ── */
.close-banner{border:1.5px solid #fbbf24;border-radius:12px;padding:.875rem 1.1rem;margin-bottom:.75rem;}

/* ── Hover effects on interactive elements ── */
.stButton button{border-radius:8px;font-weight:500;transition:all .2s;}
.stButton button:hover{transform:translateY(-1px);box-shadow:0 4px 12px rgba(0,0,0,.25);}
.stTextInput input,.stTextArea textarea{border-radius:8px !important;}
.stTextInput input:focus,.stTextArea textarea:focus{border-color:#60a5fa !important;box-shadow:0 0 0 3px rgba(96,165,250,.2) !important;}
</style>""", unsafe_allow_html=True)


def page_header(title, subtitle=""):
    st.markdown(f'<div class="ph"><h2>{title}</h2>{"<p>"+subtitle+"</p>" if subtitle else ""}</div>',
                unsafe_allow_html=True)


def metric_card(label, value, color=""):
    st.markdown(f'<div class="mc {color}"><div class="v">{value}</div><div class="l">{label}</div></div>',
                unsafe_allow_html=True)


_S = {"Pending":"b-pending","Assigned":"b-assigned","In Progress":"b-inprogress","Resolved":"b-resolved","Closed":"b-closed"}
_P = {"Low":"b-low","Medium":"b-medium","High":"b-high","Critical":"b-critical"}
_SE = {"Pending":"⏳","Assigned":"📌","In Progress":"🔄","Resolved":"✅","Closed":"🔒"}
_PE = {"Low":"🟢","Medium":"🟡","High":"🔴","Critical":"🔥"}

def status_badge(s):   return f'<span class="badge {_S.get(s,"b-pending")}">{_SE.get(s,"")} {s}</span>'
def priority_badge(p): return f'<span class="badge {_P.get(p,"b-medium")}">{_PE.get(p,"")} {p}</span>'


def render_timeline(history):
    if not history: st.info("No activity recorded yet."); return
    html = '<div style="padding:.4rem 0;">'
    for i, ev in enumerate(history):
        last   = i == len(history) - 1
        action = ev.get("action","Update")
        ts     = str(ev.get("timestamp",""))[:16]
        note   = ev.get("note","")
        old_s  = ev.get("old_status","")
        new_s  = ev.get("new_status","")
        dc = "res" if new_s=="Resolved" else "cls" if new_s=="Closed" else ""
        sc = f'<span style="font-size:.72rem;opacity:.55;">{old_s} → {new_s}</span>' if old_s and new_s else ""
        nh = f'<div class="tl-note">{note}</div>' if note else ""
        lh = '<div class="tl-line"></div>' if not last else ""
        html += f'''<div class="tl-item">
          <div style="position:relative;flex-shrink:0;padding-top:4px;">
            <div class="tl-dot {dc}"></div>{lh}
          </div>
          <div>
            <div class="tl-action">{action}</div>
            <div class="tl-meta">📅 {ts} &nbsp;•&nbsp; {sc}</div>
            {nh}
          </div>
        </div>'''
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def render_progress_tracker(current_status):
    steps = ["Pending","Assigned","In Progress","Resolved","Closed"]
    try: ci = steps.index(current_status)
    except: ci = 0
    html = '<div class="pt">'
    for i, step in enumerate(steps):
        if i < ci:   cc, lc, icon = "done", "done", "✓"
        elif i == ci: cc, lc, icon = "cur",  "cur",  str(i+1)
        else:         cc, lc, icon = "",     "",     str(i+1)
        html += f'<div class="pt-step"><div class="pt-circle {cc}">{icon}</div><div class="pt-label {lc}">{step}</div></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
