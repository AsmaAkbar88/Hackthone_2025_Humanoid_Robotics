🔹 Step 1: PowerShell ko Administrator mein open karein

```bash
https://minikube.sigs.k8s.io/docs/start/?arch=%2Fwindows%2Fx86-64%2Fstable%2F.exe+download ```

Start Menu par click karein

Search karein PowerShell

Windows PowerShell par right-click karein

Run as Administrator par click karein

Agar Yes / No poochay → Yes kar dein

⚠️ Ye step bohot zaroori hai

# Minikube Installation Guide on Windows

✅ **Step 1: Create folder**  
Yeh command run karein:

```powershell
# C:\minikube naam ka folder ban jayega
New-Item -ItemType Directory -Path C:\minikube 

🔹 Step 2: Download Minikube with progress

Alternative command use karein, jisme progress percentage dikhega:

Invoke-WebRequest `
  -Uri "https://github.com/kubernetes/minikube/releases/latest/download/minikube-windows-amd64.exe" `
  -OutFile "C:\minikube\minikube.exe"


  ✅ Step 3: Verify download
Jab download complete ho jaye, PowerShell automatically next line par aa jayega (cursor blink karega).

Ab check karein:

dir C:\minikube

minikube.exe file wahan visible honi chahiye.

🔹 Step 4: Check Minikube version

minikube version

👉 Agar version show ho jaye:
🎉 Minikube successfully installed!

 minikube start

 thora time ly ga or image bna day ga or docker ko on rkhna zrori hy 

 ----------------------------------------------------------------------------------


 # Helm Installation on Windows 🪟

Aap **Windows user** hain → **YEH WALA OPTION LENA HAI**  

✅ **From Winget (Windows)** ⭐  
सब से easy & safe

---

## Step 1: Install Helm

👉 Command run karein:

```powershell
winget install Helm.Helm

Jab prompt aaye → Y press karein

Internet chalay ga → 1–2 minute lag sakte hain

Step 2: Verify Installation
helm version

Agar output aaye, jaise:

version.BuildInfo{Version:"v4.x.x", ...}

🎉 Helm successfully installed ✅

Step 3: Create a new Helm project

🔹 Ab sirf yeh command run karein (cd mat likhein):

helm create todo-chatbot

-----------------------------------------------------------------------------------

##Install and Set Up kubectl on Windows

https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/

curl.exe -LO "https://dl.k8s.io/release/v1.35.0/bin/windows/amd64/kubectl.exe"

kubectl version
