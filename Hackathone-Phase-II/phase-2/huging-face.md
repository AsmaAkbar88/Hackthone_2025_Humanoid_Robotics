# Git & Hugging Face Setup Guide

## 🟢 STEP-1: Purane Git credentials REMOVE karein (sab se pehle)
Terminal / Command Prompt mein sirf yeh aik command likhein:

```bash
git config --global --unset credential.helper  ```

Expected result:

Koi error na aaye

Ya kuch output na ho (blank rehna bilkul normal hai)

Ab aap kya karein:

Command chala kar sirf yeh likh kar reply karein:

👉 “STEP-1 DONE”


Done:
STEP-1 DONE ✔️
___________________________________________________________

🟢 STEP-2: Purana Git remote REMOVE karein

Terminal / Command Prompt mein sirf yeh command likhein:
```bash
git remote remove origin```

Expected result:

Koi error nahi aana chahiye

Agar output blank ho, to woh bilkul theek hai

Ya agar error aaye to error ka exact text paste karo

reply me:

Error example (good news):

error: No such remote: 'origin'

Iska matlab hai ke repo mein pehle se koi origin remote maujood hi nahi

Hum maan lete hain ke koi purana remote nahi hai

🟢 STEP-2 ka result: ✔️ PASS / CLEAR
________________________________________________________

🟢 STEP-3: Check karein koi remote hai ya nahi

Terminal mein sirf yeh aik command likhein:

git remote -v

Expected result:

Ya to kuch bhi output nahi aayega

Ya koi remote dikhega (agar hoga)

Ab kya karna hai:

Command chala kar jo output aaye, bilkul copy-paste karke yahin bhej dein

Output example:
(blank)

Blank output ka matlab hai repo clean state mein hai
________________________________________________________

🟢 STEP-4: SIRF sahi remote ADD karein

Terminal mein sirf yeh aik command likhein:

git remote add origin https://huggingface.co/spaces/asmaakbar/phase-ll.git

Expected result:

Koi error nahi aani chahiye

Output blank rehna normal hai

Done:
STEP-4 DONE ✔️
________________________________________________________

🟢 STEP-5: Remote verify karein

Terminal mein sirf yeh aik command likhein:

git remote -v

Expected result:

origin  https://huggingface.co/spaces/asmaakbar/phase-ll.git (fetch)
origin  https://huggingface.co/spaces/asmaakbar/phase-ll.git (push)

Ab kya karein:

Command chalao aur jo output aaye, bilkul copy-paste kar ke bhej do

Done example:

origin  https://huggingface.co/spaces/asmaakbar/phase-ll.git (fetch)
origin  https://huggingface.co/spaces/asmaakbar/phase-ll.git (push)


STEP-5 PERFECT ✔️
________________________________________________________

🟢 STEP-6: Hugging Face par dobara CLEAN login (token)

Terminal mein sirf yeh aik command likhein:

hf auth logout

Expected result:

Logout successful ka message aana chahiye

Ya koi simple confirmation

Ab kya karein:

Command chalao phir sirf yeh reply karo:

👉 “STEP-6 DONE”

Done example:

Successfully logged out from all access tokens.

STEP-6 DONE ✔️
________________________________________________________

🟢 STEP-7: Hugging Face login (NEW / WRITE token)

Terminal mein sirf yeh aik command likhein:

hf auth login --add-to-git-credential

Instructions:

Jab pooche: Enter your token (input will not be visible)

Hugging Face website se WRITE permission wala token paste karein

Right-Click se paste karein (Ctrl+V kaam nahi karega)

Jab pooche: Add token as git credential? [y/N]

y likhein aur Enter press karein

Expected result:

Login successful ka message

Koi error nahi aani chahiye

Ab kya karein:

Yeh step complete kar ke exact jo output aaye, wahi yahan paste kar dein

❌ Abhi:

git push

commit

kuch bhi nahi

