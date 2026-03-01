📁 Folder Structure aur Unka Kaam

    1. `/Inbox` - File Drop Zone
     - Kab use hota hai: Jab aap koi naya file daalte ho
     - Kya hota hai: Watcher detect karta hai aur /Needs_Action mein copy karta hai
     - Example:
     1   Inbox/my_invoice.pdf → Needs_Action/FILE_DROP_my_invoice.md

    ---

    2. `/Needs_Action` - Pending Tasks
     - Kab use hota hai: Jab koi task AI ko process karna ho
     - Kya hota hai: Orchestrator uthata hai aur Claude Code ko bhejta hai
     - Example:
     1   Needs_Action/FILE_DROP_invoice.md → Claude processes → Done/

    ---

    3. `/Plans` - AI Generated Plans ⭐
     - Kab use hota hai: Jab Claude Code koi plan banata hai
     - Kya hota hai: Claude step-by-step plan likhta hai
     - Example:
      1   # /Plans/PLAN_Reply_Client_Email_2026-02-28.md
      2
      3   ## Objective
      4   Reply to client inquiry about pricing
      5
      6   ## Steps
      7   - [x] Read client email
      8   - [x] Check pricing from Company Handbook
      9   - [ ] Draft reply
     10   - [ ] Send for approval
     11   - [ ] Move to Done
     - Kab banega: Silver Tier mein (jab Claude properly plans banayega)

    ---

    4. `/Pending_Approval` - Human Approval Required ⚠️
     - Kab use hota hai: Jab Claude ko koi sensitive action karna ho
     - Kya hota hai: Claude approval request file banata hai
     - Example:
     1   # /Pending_Approval/APPROVAL_Send_Email_Client_A.md
     2
     3   ---
     4   action: send_email
     5   to: client@example.com
     6   subject: Invoice #123
     7   ---
     8
     9   Ready to send. Move to /Approved to proceed.
     - Aapka kaam: File ko /Approved ya /Rejected mein move karo

    ---

    5. `/Approved` - Approved Actions ✅
     - Kab use hota hai: Jab aap koi action approve karte ho
     - Kya hota hai: Orchestrator detect karta hai aur action execute karta hai
     - Example:
     1   Pending_Approval/APPROVAL_Send_Email.md → (you move) → Approved/
     2   Orchestrator → Sends email → Moves to Done/

    ---

    6. `/Rejected` - Rejected Actions ❌
     - Kab use hota hai: Jab aap koi action reject karte ho
     - Kya hota hai: Orchestrator task cancel karta hai
     - Example:
     1   Pending_Approval/APPROVAL_Payment.md → (you move) → Rejected/
     2   Orchestrator → Logs rejection → Moves to Done/

    ---

    7. `/Done` - Completed Tasks ✅
     - Kab use hota hai: Jab task complete ho jata hai
     - Kya hota hai: Files archive ho jati hain
     - Example:
     1   Needs_Action/task.md → Done/task.md

    ---

    8. `/Logs` - Operation Logs 📝
     - Kab use hota hai: Har operation log hota hai
     - Kya hota hai: Daily logs save hote hain
     - Example:
     1   Logs/orchestrator_2026-02-28.log
     2   Logs/2026-02-28.json

    ---

    🔄 Complete Flow Diagram

      1 ┌─────────────────────────────────────────────────────────────┐
      2 │                    COMPLETE FLOW                            │
      3 └─────────────────────────────────────────────────────────────┘
      4
      5 1. USER drops file
      6    ↓
      7    Inbox/myfile.txt
      8
      9 2. WATCHER detects & copies
     10    ↓
     11    Needs_Action/FILE_DROP_myfile.md
     12    Needs_Action/FILE_DROP_myfile.txt
     13
     14 3. ORCHESTRATOR picks up
     15    ↓
     16    Claude Code processes
     17    ↓
     18    Creates plan (optional)
     19    ↓
     20    Plans/PLAN_myfile.md
     21
     22 4. CLAUDE checks if approval needed
     23    │
     24    ├── NO approval needed ──→ Done/
     25    │
     26    └── YES approval needed
     27          ↓
     28          Pending_Approval/APPROVAL_action.md
     29
     30 5. HUMAN reviews
     31    │
     32    ├── Move to /Approved ──→ Orchestrator executes ──→ Done/
     33    │
     34    └── Move to /Rejected ──→ Task cancelled ──→ Done/

    ---

    📅 Kab Kaunsa Folder Use Hoga?


    ┌─────────────────────────────┬─────────────────────────────────────────────────────────────────────┐
    │ Scenario                    │ Flow                                                                │
    ├─────────────────────────────┼─────────────────────────────────────────────────────────────────────┤
    │ Simple file processing      │ Inbox → Needs_Action → Done                                         │
    │ Email reply (non-sensitive) │ Inbox → Needs_Action → Claude drafts → Plans/ → Done                │
    │ Email send (needs approval) │ Inbox → Needs_Action → Pending_Approval → (you: Approved) → Done      │
    │ Payment request             │ Inbox → Needs_Action → Pending_Approval → (you: Rejected) → Rejected/ │
    │ Multi-step task             │ Inbox → Needs_Action → Plans/ → Done                                │
    └─────────────────────────────┴─────────────────────────────────────────────────────────────────────┘

    ---

    🎯 Bronze Tier vs Silver/Gold Tier

    Bronze Tier (Current)
     - ✅ Inbox → Needs_Action → Done (Working!)
     - ⚠️ Plans folder: Abhi properly use nahi ho raha
     - ⚠️ Pending_Approval: Abhi implement nahi hua

    Silver Tier (Next)
     - ✅ Plans folder properly use hoga
     - ✅ Pending_Approval workflow
     - ✅ Human-in-the-loop approval

    Gold Tier (Advanced)
     - ✅ Full approval workflow
     - ✅ MCP servers for actions
     - ✅ Ralph Wiggum loop

    ---

    🚀 Summary


    ┌───────────────────┬──────────┬─────────┬─────────┐
    │ Folder            │ Bronze   │ Silver  │ Gold    │
    ├───────────────────┼──────────┼─────────┼─────────┤
    │ /Inbox            │ ✅       │ ✅      │ ✅      │
    │ /Needs_Action     │ ✅       │ ✅      │ ✅      │
    │ /Done             │ ✅       │ ✅      │ ✅      │
    │ /Plans            │ ⚠️ Basic │ ✅ Full │ ✅ Full │
    │ /Pending_Approval │ ❌       │ ✅      │ ✅      │
    │ /Approved         │ ❌       │ ✅      │ ✅      │
    │ /Rejected         │ ❌       │ ✅      │ ✅      │
    └───────────────────┴──────────┴─────────┴─────────┘

    ---