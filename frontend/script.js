(function(){
const BASE=(window.APP_CONFIG||{}).BACKEND_BASE||location.origin.replace("5500","8000");
const strictEl=document.getElementById("strictMode");
const imgInput=document.getElementById("imgInput");
const imgThr=document.getElementById("imgThreshold"); const imgTVal=document.getElementById("imgTVal");
const imgBtn=document.getElementById("imgBtn"); const imgOut=document.getElementById("imgOut");
const txtInput=document.getElementById("txtInput"); const txtThr=document.getElementById("txtThreshold"); const txtTVal=document.getElementById("txtTVal");
const txtBtn=document.getElementById("txtBtn"); const txtOut=document.getElementById("txtOut");
imgThr.oninput=()=>imgTVal.textContent=imgThr.value;
txtThr.oninput=()=>txtTVal.textContent=txtThr.value;
imgBtn.onclick=async()=>{
 if(!imgInput.files.length)return;
 const fd=new FormData();
 fd.append("file",imgInput.files[0]);
 fd.append("threshold",imgThr.value);
 fd.append("strict",strictEl.checked);
 imgOut.textContent="Uploading…";
 try{
  const r=await fetch(BASE+"/api/detect-image",{method:"POST",body:fd});
  imgOut.textContent=JSON.stringify(await r.json(),null,2);
 }catch(e){imgOut.textContent="Error "+e}
};
txtBtn.onclick=async()=>{
 const payload={text:txtInput.value,threshold:parseFloat(txtThr.value),strict:strictEl.checked};
 txtOut.textContent="Sending…";
 try{
  const r=await fetch(BASE+"/api/detect-text",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});
  txtOut.textContent=JSON.stringify(await r.json(),null,2);
 }catch(e){txtOut.textContent="Error "+e}
};
})(); 
