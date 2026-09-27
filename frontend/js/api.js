const API="http://localhost:5000/api";
function token(){return localStorage.getItem("token")}
function authHeaders(json=true){const h={}; if(json) h["Content-Type"]="application/json"; if(token()) h.Authorization="Bearer "+token(); return h}
async function api(path,options={}){options.headers={...authHeaders(options.body!==undefined),...(options.headers||{})}; const r=await fetch(API+path,options); let d={}; try{d=await r.json()}catch{} if(r.status===401){localStorage.removeItem("token"); location.href="login.html"} if(!r.ok) throw new Error(d.error||"Request failed"); return d}
function requireAuth(){if(!token()) location.href="login.html"}
