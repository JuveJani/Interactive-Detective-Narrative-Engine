#!/usr/bin/env python3
"""Generate expanded PLAYER markdown and mapping manifest for The Cold Storage Alarm.

This script renders the single-investigator PLAYER package from the adventure's
approved canon (fixed truth, timeline, NPC knowledge, object interactions,
capability checks, investigation flow, and endings). It does not invent new
facts, times, evidence, NPC knowledge boundaries, check logic, or ending logic;
it only writes richer player-facing prose around the already-approved content
and emits the unit -> file/anchor mapping manifest consumed by downstream
tooling.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADV = ROOT / "adventures" / "The_Cold_Storage_Alarm"
ADVENTURE = ADV / "adventure"
PLAYER = ADVENTURE / "PLAYER"
DNR = ADVENTURE / "DO_NOT_READ"

DEFAULT_TOPIC_TIME_MIN = 2

TOPIC_RETURN_CHOICES: dict[str, list[str]] = {
    "UNIT-ELENA": [
        "Return to the Elena conversation menu.",
        "Return to the loading dock.",
    ],
    "UNIT-WORKER": ["Return to the dock worker conversation menu.", "Return to the loading dock."],
    "UNIT-PAT": ["Return to the dock worker conversation menu.", "Return to the loading dock."],
    "UNIT-DEV": ["Return to the dock worker conversation menu.", "Return to the loading dock."],
    "UNIT-MARCUS": ["Return to the security office.", "Return to the loading dock."],
    "UNIT-LORI": ["Return to the manager office.", "Return to the loading dock."],
}


def _load_npc_topic_times() -> dict[str, int]:
    npc = json.loads((DNR / "npc_investigation_package.json").read_text(encoding="utf-8"))
    times: dict[str, int] = {}
    for conv in npc.get("conversation_graph", []) or []:
        for node in conv.get("nodes", []) or []:
            uid = node.get("npc_response_unit", "")
            if uid and node.get("time_cost_minutes") is not None:
                times[uid] = int(node["time_cost_minutes"])
    return times


def _topic_time_meta(unit_id: str, topic_times: dict[str, int]) -> str:
    minutes = topic_times.get(unit_id, DEFAULT_TOPIC_TIME_MIN)
    return f"**Time cost:** {minutes} min"


def _topic_choices(unit_id: str) -> list[str]:
    for prefix, choices in TOPIC_RETURN_CHOICES.items():
        if unit_id.startswith(prefix + "-") or unit_id == prefix:
            return list(choices)
    return ["Return to your current location menu or continue the conversation."]


def human_title(uid: str) -> str:
    s = uid
    for prefix in ("UNIT-CHK-", "UNIT-", "SC-", "INF-", "END-", "REC-"):
        if s.startswith(prefix):
            s = s[len(prefix):]
            break
    return re.sub(r"\s+", " ", s.replace("-", " ")).strip().capitalize()


def unit_block(uid: str, body: str, choices: list[str] | None = None, meta: str = "", title: str | None = None) -> str:
    display = title or human_title(uid)
    slug = uid.lower()
    lines = [f"<!-- unit:{slug} -->", f"### {display}", ""]
    if meta:
        lines.append(meta)
        lines.append("")
    lines.append(body.strip())
    lines.append("")
    if choices:
        lines.append("**What do you do?**")
        lines.append("")
        for c in choices:
            lines.append(f"- {c}")
        lines.append("")
    return "\n".join(lines)


def write_player_files() -> dict[str, dict]:
    mapping: dict[str, dict] = {}
    buckets: dict[str, list[str]] = {}

    def add(uid: str, fname: str, body: str, choices: list[str] | None = None, meta: str = "", title: str | None = None) -> None:
        block = unit_block(uid, body, choices, meta, title)
        buckets.setdefault(fname, []).append(block)
        mapping[uid] = {"file": f"PLAYER/{fname}", "anchor": title or human_title(uid), "unit_id": uid}

    # ------------------------------------------------------------------
    # Top-level orientation files (structure preserved from prior release)
    # ------------------------------------------------------------------

    (PLAYER / "OPENING.md").write_text(
        """You arrive at the **loading dock** of the Northline cold-chain warehouse at **1:00 a.m.** on Friday, March 13.

Supervisor **Elena Morales** called you in as the on-call **refrigeration technician**. A high-temperature alarm on cold zone CZ-1 sounded at **11:30 p.m.** Supply air in the cold storage hall is still rising. If CZ-1 stays above the compliance threshold until **5:00 a.m.**, the facility must begin a product write-off and notify health regulators.

Your job tonight is to find why staging control failed, who had access, and whether receiving records explain any discrepancies—before the compliance deadline closes the shift.
""",
        encoding="utf-8",
    )

    (PLAYER / "HOW_TO_PLAY.md").write_text(
        """# How to Play — The Cold Storage Alarm

**Mode:** Single investigator (you play the on-call technician).

**Time:** Each action shows a time cost in minutes. The in-world clock moves forward. You cannot travel back to an earlier time.

**Checks:** Some actions require a d20 roll plus your character modifier. Each check allows **one attempt**. Success and failure use separate result text.

**Notes:** Record facts you learn. Synthesis steps ask you to connect records you have already found—answers are not delivered automatically.

**Deadline:** At **5:00 a.m.**, compliance procedures may end your investigation window.

**Before you start:** read your character sheet for your check modifiers, and keep your case file open beside you to log clues as you find them.

Read the opening section first, then use each location's base section in the locations file as your menu at that place.
""",
        encoding="utf-8",
    )

    (PLAYER / "README.md").write_text(
        """# The Cold Storage Alarm — Player Package

**Mode:** Single investigator
**Estimated playtime:** About two hours
**In-world duration:** One night shift (roughly four hours)

Read only files in this folder. Do not open `DO_NOT_READ/` or other repository paths.

This package also includes a character sheet with your check modifiers and a blank case file template for logging clues, alongside the usual location, object, people, scene, inference, recovery, and ending sections.

Start with the opening section, then the how-to-play notes. Follow section prompts in order; do not read ahead in ending sections.
""",
        encoding="utf-8",
    )

    (PLAYER / "NAVIGATION_INDEX.md").write_text(
        """# Navigation index

Do not read ahead in these files.

- Opening briefing uses the opening file.
- Your stats and check modifiers use the character sheet file.
- Clue notes and working theories use the case file template.
- Base locations use the locations file.
- Object results use the objects file.
- People on site use the people file.
- Time scenes use the scenes file.
- Inference worksheets use the inference file.
- Recovery prompts use the recovery file.
- Endings use the endings file.
""",
        encoding="utf-8",
    )

    # ------------------------------------------------------------------
    # New solo-mode reference sheets (no unit anchors — reference material,
    # not branching narrative units)
    # ------------------------------------------------------------------

    (PLAYER / "CHARACTERS").mkdir(parents=True, exist_ok=True)
    (PLAYER / "CHARACTERS" / "CHARACTER_SHEET.md").write_text(
        """# Character sheet — on-call refrigeration technician

You are the on-call refrigeration technician for the Northline cold-chain warehouse. You know compressor staging, BMS terminals, and cold-chain compliance rules well enough that Elena calls you first when CZ-1 misbehaves at 1:00 a.m. You are not a police investigator, an auditor, or an interrogator — whatever you find tonight, you find it by checking records, checking equipment, and asking straight questions.

## Check modifiers

When a scene calls for a check, roll **1d20** and add the modifier for the listed capability. Compare your total against the difficulty noted in that scene — the target number is not shown to you in advance, and each check allows **one attempt**. A failed check never ends your investigation; it just means that particular thread stays closed and you rely on another record instead.

| Capability | Modifier | When it applies |
|---|---|---|
| **Perception** | **+3** | Close physical searches — hardware wear, adhesive residue, locker contents, anything you have to look hard for. |
| **Technical** | **+3** | Operating engineering systems — BMS exports, terminal menus, anything that runs on the automation network. |
| Reasoning | +2 | Reading and connecting records once you already hold them. |
| Persuasion | +1 | Getting someone to open up further in conversation. |
| Intimidation | +0 | Pressuring someone who is already being evasive. |
| Agility | +1 | Physical movement under time pressure. |
| Strength | +1 | Manual tasks requiring force. |

Your training runs toward **perception** and **technical** work — a career spent noticing what's slightly out of place on refrigeration hardware and BMS logs. You are competent in conversation but no specialist interrogator, which is reflected in your lower social modifiers.

## Equipment

- Facility-issued flashlight and multitool
- Two-way radio (direct line to Elena and the security desk)
- Photo ID and your own after-hours access badge
- A notepad — use `PLAYER/SHARED/CASE_FILE.md` as your case file template

## Personal stakes

Every hour CZ-1 stays above threshold is an hour closer to a product write-off and a compliance notification that will follow the facility for months. You were called in to fix the equipment and explain what happened — in that order.
""",
        encoding="utf-8",
    )

    (PLAYER / "SHARED").mkdir(parents=True, exist_ok=True)
    (PLAYER / "SHARED" / "CASE_FILE.md").write_text(
        """# Case file

Use this template to log what you learn. Nothing here is filled in for you — the investigation only works if you write down what you actually find.

## Incident summary

- Alarm first sounded: ______________________
- Your arrival time: ______________________
- Compliance deadline: ______________________
- Zone affected: ______________________

## Timeline log

Record each timestamp you confirm, in the order you learn it (not necessarily the order it happened).

| Time | What happened | Source |
|---|---|---|
| | | |
| | | |
| | | |
| | | |
| | | |

## People contacted

| Person | Role | Topics covered | Still to ask |
|---|---|---|---|
| Marcus Hale | Night security guard | | |
| Dev Santos | Refrigeration contractor | | |
| Lori Okonkwo | Logistics coordinator | | |
| Elena Morales | On-call supervisor | | |
| Pat Nguyen | Cleaning crew lead | | |
| Records desk | Badge archive policy | | |

## Evidence log

| Record or object | What it shows | Where you found it |
|---|---|---|
| | | |
| | | |
| | | |
| | | |
| | | |

## Working theory

- **What happened:** ______________________________________________
- **How it happened:** ______________________________________________
- **Who is accountable:** ______________________________________________
- **Why:** ______________________________________________

## Inference tracker

Mark each worksheet once you have attempted it. A checked box does not mean you succeeded — only that you have reached a conclusion, right or wrong.

- [ ] Badge misattributed
- [ ] Staging root cause
- [ ] Relabel fraud
- [ ] Control access mismatch
- [ ] Culprit supported
- [ ] Perfect reconstruction

## Final accountability statement (draft)

Write your answer to each accusation question here before you commit to it.

- **Who is accountable for the unauthorized actions tonight?** ______________________________________________
- **What mechanism suspended cold-chain staging?** ______________________________________________
- **What primary operational failure caused product-risk escalation?** ______________________________________________
- **Who had motive tied to inbound manifest discrepancies?** ______________________________________________
""",
        encoding="utf-8",
    )

    # ------------------------------------------------------------------
    # Locations — richer atmosphere per hub; choice menus preserved exactly
    # ------------------------------------------------------------------

    add(
        "UNIT-DOCK-BASE",
        "LOCATIONS.md",
        "The loading dock is lit by sodium fixtures. Forklifts sit idle. Elena Morales watches the bay doors while staff move between the dock and the office wing. "
        "Cold rolls off the bay in waves whenever a door cycles, and the smell of diesel and refrigerant hangs in the air. Somewhere past 1:00 a.m., the building has settled into the strange quiet of a shift that has already gone wrong. "
        "As you learn the site layout and supervisor constraints, additional routes and briefing options become available here.",
        [
            "Talk to Elena Morales.",
            "Walk through the dock corridor to the cold storage hall.",
            "Talk to a dock worker.",
            "Head inside to the staff break room.",
            "Cut through the warehouse corridor to the security office.",
            "Take the office wing corridor to the warehouse manager office.",
            "Review the supervisor briefing area.",
            "Request escort clearance to the automation control room.",
            "Receive supervisor briefing at the loading dock.",
            "Survey the dock and adjacent corridors.",
            "Prepare final accountability documentation before the compliance threshold.",
            "Work under supervisor dock restriction enforcement.",
        ],
        "**Location:** Loading dock | **Time cost:** 0 min",
        "Loading dock",
    )

    add(
        "UNIT-DOCK-ELENA-HUB",
        "NPCS.md",
        "Elena Morales meets you at the briefing table near the bay doors. Her clipboard already holds the alarm timeline, and she answers in the clipped tone of someone coordinating an emergency response.",
        [
            "Ask where the investigation should begin.",
            "Ask whether a map or site overview is available.",
            "Ask who was still on site working late.",
            "Return to the loading dock.",
        ],
        "**Location:** Loading dock | **Time cost:** 1 min",
        "Talk to Elena Morales",
    )

    add(
        "UNIT-DOCK-WORKER-HUB",
        "NPCS.md",
        "A dock worker pauses between the idle forklifts — Pat Nguyen with a mop cart, and Dev Santos arriving from the parking lot with a tool bag. Either can spare a minute between tasks.",
        [
            "Ask what they know about the incident.",
            "Ask their name and role on site.",
            "Ask how long they have worked here.",
            "Ask who or what they know locally.",
            "Return to the loading dock.",
        ],
        "**Location:** Loading dock | **Time cost:** 1 min",
        "Talk to a dock worker",
    )

    add(
        "UNIT-ELENA-BEGIN",
        "NPCS.md",
        "Elena taps the incident timeline on her clipboard. "
        '"Start with cold storage and staging control. Security can pull badge records after the archive sync if you need access history."',
        ["Return to the Elena conversation menu.", "Return to the loading dock."],
        "**Time cost:** 2 min",
        "Where to begin",
    )

    add(
        "UNIT-ELENA-MAP",
        "NPCS.md",
        "Elena pulls a folded site map from the briefing table and marks the cold hall, security office, and manager wing. "
        '"Use this for corridors you have not walked yet. I can escort you to control if engineering access is required."',
        ["Return to the Elena conversation menu.", "Return to the loading dock."],
        "**Time cost:** 2 min",
        "Site overview",
    )

    add(
        "UNIT-WORKER-ROLE",
        "NPCS.md",
        "Pat Nguyen sets the mop cart aside. "
        '"Pat Nguyen — dock sanitation and floor prep. I am on the late crew when receiving runs long."',
        ["Return to the dock worker conversation menu.", "Return to the loading dock."],
        "**Time cost:** 2 min",
        "Name and role",
    )

    add(
        "UNIT-WORKER-TENURE",
        "NPCS.md",
        "Pat thinks for a moment. "
        '"About three years on this dock. I know the cold hall doors and which bays stay open after midnight."',
        ["Return to the dock worker conversation menu.", "Return to the loading dock."],
        "**Time cost:** 2 min",
        "Time on site",
    )

    add(
        "UNIT-WORKER-LOCAL",
        "NPCS.md",
        "Pat nods toward the office wing and the break room corridor. "
        '"Elena runs the shift. Lori stays at receiving when manifests jam. Marcus does rounds from security."',
        ["Return to the dock worker conversation menu.", "Return to the loading dock."],
        "**Time cost:** 2 min",
        "Local contacts",
    )

    add(
        "UNIT-COLD-BASE",
        "LOCATIONS.md",
        "Cold air rolls from the hall doors. Pallet rows stretch toward zone CZ-1. "
        "Your breath fogs the moment you step past the threshold, and the compressor hum overhead sounds one register lower than it should. CZ-1's supply air display glows at the far end of the hall like it is keeping score.",
        [
            "Examine the cold storage door latch and reader.",
            "Walk the length of aisle C between the pallet rows.",
            "Read the live CZ-1 supply air temperature display.",
            "Follow the engineering passage to the automation control room.",
            "Return to the loading dock.",
            "Return toward the break room corridor.",
        ],
        "**Location:** Cold storage hall | **Time cost:** 0 min",
        "Cold storage hall",
    )

    add(
        "UNIT-CONTROL-BASE",
        "LOCATIONS.md",
        "The automation control room holds engineering workstations and a CZ-1 staging indicator panel. "
        "Server fans hum steadily under the fluorescent light, and rows of status LEDs blink through their normal patterns — except for one panel that is not blinking at all.",
        [
            "Approach the engineering workstation.",
            "Inspect the CZ-1 staging indicator panel.",
            "Return to the cold storage hall.",
            "Return to the loading dock with the supervisor.",
            "Return to the security office.",
        ],
        "**Location:** Automation control room | **Time cost:** 0 min",
        "Automation control room",
    )

    add(
        "UNIT-SECURITY-BASE",
        "LOCATIONS.md",
        "The security office holds an alarm panel and a badge archive terminal. "
        "A wall of small monitors cycles through empty hallways, and the alarm panel's speaker occasionally clicks like it is about to say something before falling silent again.",
        [
            "Review recent alarm history on the security panel.",
            "Open the badge access archive terminal.",
            "Return to the loading dock.",
            "Return to the break room.",
        ],
        "**Location:** Security office | **Time cost:** 0 min",
        "Security office",
    )

    add(
        "UNIT-MANAGER-BASE",
        "LOCATIONS.md",
        "The warehouse manager office is open for the emergency. Lori Okonkwo's receiving workstation still shows an active reconciliation screen. "
        "Stacks of manifest printouts cover most of the desk, and the fluorescent light overhead flickers just enough to notice. Lori has not left this chair in longer than tonight's alarm alone would explain.",
        [
            "Review the open receiving reconciliation screen.",
            "Speak with Lori Okonkwo about receiving and access topics you have unlocked.",
            "Return to the loading dock.",
            "Return to the break room.",
        ],
        "**Location:** Warehouse manager office | **Time cost:** 0 min",
        "Warehouse manager office",
    )

    add(
        "UNIT-BREAK-BASE",
        "LOCATIONS.md",
        "The staff break room has vending machines, lockers, and a window toward the dock. "
        "The vending machines hum against one wall, and a half-finished cup of coffee sits abandoned on the table, gone cold along with everything else tonight.",
        [
            "Walk along the staff locker bank.",
            "Look out toward the dock loading area.",
            "Return to the loading dock.",
            "Walk to the manager office through the staff corridor.",
            "Follow the interior hallway to the security office.",
            "Take the side passage toward the cold storage hall.",
        ],
        "**Location:** Staff break room | **Time cost:** 0 min",
        "Staff break room",
    )

    # ------------------------------------------------------------------
    # Objects — setup + approved result (unchanged) + return context.
    # The middle sentence(s) in every triple below are the original,
    # approved facts and are left verbatim.
    # ------------------------------------------------------------------

    def obj(setup: str, fact: str, ret: str) -> str:
        return f"{setup} {fact} {ret}"

    object_units = [
        ("UNIT-DOCK-BRIEFING-MENU", obj(
            "You step up to the briefing table where Elena has laid out everything she has gathered so far.",
            "Elena points to a printed incident timeline on the briefing table.",
            "You note the timeline before stepping back toward the bay doors.",
        ), ["Return to the loading dock."], "**Time cost:** 2 min", "Supervisor briefing"),
        ("UNIT-ESCORT-GRANTED", obj(
            "Elena does not argue when you ask for control room access — she just reaches for the escort log.",
            "Elena signs an escort log and walks you toward the engineering passage.",
            "With her signature down, you are cleared to make the walk on your own from here.",
        ), ["Return to the loading dock."], "**Time cost:** 3 min", "Escort granted"),
        ("UNIT-COLD-DOOR-MENU", obj(
            "Frost rimes the frame where the cold storage door meets the corridor air.",
            "The cold storage door has a badge reader and a heavy latch.",
            "Whatever you decide to check, the door itself is not going anywhere.",
        ), ["Check the latch hardware for recent disturbance.", "Return to the cold storage hall."], "**Time cost:** 3 min", "Cold storage door"),
        ("UNIT-LATCH-SUCCESS", obj(
            "You crouch and run a light along the latch plate, looking past the obvious.",
            "Under the latch plate you notice fresh scuffing where hardware was recently handled.",
            "You note the wear pattern before straightening up and returning to the door.",
        ), ["Return to the cold storage door menu."], "**Time cost:** 4 min", "Latch check — success"),
        ("UNIT-LATCH-FAIL", obj(
            "You crouch and check the latch plate as carefully as the light allows.",
            "The latch hardware looks ordinary from this angle; nothing useful stands out.",
            "Nothing here changes what you already knew, so you head back to the door.",
        ), ["Return to the cold storage door menu."], "**Time cost:** 4 min", "Latch check — failure"),
        ("UNIT-AISLE-C-MENU", obj(
            "Pallet shrink-wrap crinkles under the cold air draft as you step into the row.",
            "Aisle C runs between high pallet rows.",
            "The aisle holds still around you, waiting to be searched or left alone.",
        ), ["Search the floor and pallet faces for label adhesive residue.", "Return to the cold storage hall."], "**Time cost:** 2 min", "Aisle C"),
        ("UNIT-LABEL-SUCCESS", obj(
            "You go over the floor and pallet faces inch by inch, ignoring the cold in your fingers.",
            "You recover a strip of label backing with fresh adhesive trace.",
            "You bag the strip carefully and head back toward the aisle entrance.",
        ), ["Return to aisle C menu."], "**Time cost:** 5 min", "Label search — success"),
        ("UNIT-LABEL-FAIL", obj(
            "You go over the floor and pallet faces as closely as you can manage.",
            "The floor and pallet faces show routine warehouse wear; no distinctive trace stands out.",
            "You come up empty and step back toward the aisle entrance.",
        ), ["Return to aisle C menu."], "**Time cost:** 5 min", "Label search — failure"),
        ("UNIT-LABEL-DETAIL", obj(
            "With the backing strip in hand, you lay it next to the pallet receipt printout.",
            "You compare the recovered backing print timestamp to pallet receipt records. The timestamp does not match the original partial-pallet location.",
            "You note the mismatch in your case file before returning to the aisle.",
        ), ["Return to aisle C menu."], "**Time cost:** 4 min", "Label timestamp comparison"),
        ("UNIT-TEMP-LIVE", obj(
            "You wipe frost off the sensor display to get a clean reading.",
            "The live display reads CZ-1 supply air at a sustained rise above the cold-chain threshold.",
            "You log the number and turn back toward the rest of the hall.",
        ), ["Return to the cold storage hall."], "**Time cost:** 1 min", "Live temperature display"),
        ("UNIT-TERM-02-MENU", obj(
            "The workstation screen is still lit, exactly the way someone left it hours ago.",
            "Engineering workstation CTRL-TERM-02 is awake.",
            "The terminal is not locking itself while you decide what to open first.",
        ), [
            "Review the BMS command log on this terminal.",
            "Open the closed maintenance ticket for CZ-1.",
            "Export the CZ-1 supply air temperature trend.",
            "Return to the control room.",
        ], "**Time cost:** 1 min", "Engineering workstation"),
        ("UNIT-BMS-COMMAND", obj(
            "You open the command history and scroll back to the window around the first alarm.",
            "The command log shows CMD-CZ1-MUTE-STAGE issued at 11:22 p.m. under maintenance session SVC-REFRG-MAINT.",
            "You copy the entry into your notes and back out to the workstation menu.",
        ), ["Return to the engineering workstation menu."], "**Time cost:** 4 min", "BMS command log"),
        ("UNIT-MAINT-TICKET", obj(
            "You pull up the maintenance ticket queue and find the most recently closed entry for CZ-1.",
            "Ticket CLO-1847 closed at 6:30 p.m. with a note that session SVC-REFRG-MAINT was left unlocked.",
            "You note the closeout comment and return to the workstation menu.",
        ), ["Return to the engineering workstation menu."], "**Time cost:** 3 min", "Maintenance ticket"),
        ("UNIT-TREND-SUCCESS", obj(
            "You start the export and wait through the progress bar, watching it climb.",
            "The trend export completes. Supply air inflects upward after 11:27 p.m.",
            "You save the export locally and step back from the terminal.",
        ), ["Return to the engineering workstation menu."], "**Time cost:** 5 min", "Trend export — success"),
        ("UNIT-TREND-FAIL", obj(
            "You start the export and wait through the progress bar.",
            "The export wizard closes with an error; no trend file is saved.",
            "You close the failed dialog and step back from the terminal.",
        ), ["Return to the engineering workstation menu."], "**Time cost:** 5 min", "Trend export — failure"),
        ("UNIT-STAGING-PANEL", obj(
            "A single amber indicator on the staging panel is the only thing not blinking in sequence.",
            "The CZ-1 staging panel shows compressor staging suspended.",
            "You write down the panel state and turn back toward the room.",
        ), ["Return to the control room."], "**Time cost:** 3 min", "Staging indicator panel"),
        ("UNIT-ALARM-HISTORY", obj(
            "You scroll the alarm panel's history back past the noise of tonight's other notifications.",
            "Alarm history lists ALM-COLD-DOOR-AJAR at 11:18 p.m. and ALM-COLD-HIGH at 11:30 p.m.",
            "You copy both timestamps down before stepping back from the panel.",
        ), ["Return to the security office."], "**Time cost:** 3 min", "Alarm history"),
        ("UNIT-BADGE-ARCHIVE-MENU", obj(
            "The archive terminal's status field is the first thing you check before running any query.",
            "The badge archive terminal shows whether tonight's batch upload has finished.",
            "Whatever the sync status says, the query menu is still in front of you.",
        ), [
            "Query cold storage inbound badge entries for tonight.",
            "Query control room door entries for tonight.",
            "Pull the contractor outbound dock scan record.",
            "Return to the security office.",
        ], "**Time cost:** 2 min", "Badge archive terminal"),
        ("UNIT-BADGE-COLD-ENTRY", obj(
            "You filter the badge archive down to cold storage entries for tonight's shift.",
            "Cold storage inbound log shows credential BADGE-DEV-TEMP at 11:14 p.m.",
            "You note the credential and timestamp before returning to the archive menu.",
        ), ["Return to the badge archive menu."], "**Time cost:** 4 min", "Cold storage badge query"),
        ("UNIT-BADGE-CONTROL-ENTRY", obj(
            "You switch the filter to control room door entries for the same window.",
            "Control room entry log shows badge BADGE-LORI at 11:20 p.m.",
            "You note the badge and timestamp before returning to the archive menu.",
        ), ["Return to the badge archive menu."], "**Time cost:** 3 min", "Control room badge query"),
        ("UNIT-EXIT-SCAN", obj(
            "You pull the outbound dock scan log to check the contractor's departure.",
            "Outbound dock scan shows Dev Santos exited at 7:02 p.m.",
            "You note the exit time before returning to the archive menu.",
        ), ["Return to the badge archive menu."], "**Time cost:** 3 min", "Contractor exit scan"),
        ("UNIT-MANIFEST-MENU", obj(
            "The reconciliation screen is exactly how it was left, exception flag still lit.",
            "The receiving screen still flags manifest MNF-IN-4471.",
            "The exception is still open, waiting on whichever record you check first.",
        ), [
            "Compare manifest MNF-IN-4471 to the carrier delivery record.",
            "Cross-reference the signed carrier POD against bay assignments.",
            "Return to the manager office.",
        ], "**Time cost:** 2 min", "Receiving workstation"),
        ("UNIT-MANIFEST-GAP", obj(
            "You pull the manifest up side by side with the scanned delivery record.",
            "Manifest MNF-IN-4471 shows eight cases received while carrier POD-4471 lists forty-eight.",
            "You note the quantity gap before returning to the receiving workstation.",
        ), ["Return to the manifest menu."], "**Time cost:** 5 min", "Manifest comparison"),
        ("UNIT-POD-CROSSREF", obj(
            "You flip open the carrier POD binder to check the bay assignment against what was actually logged.",
            "The signed POD assigns the full shipment to bay C3 expecting a complete lot scan.",
            "You note the assignment before returning to the receiving workstation.",
        ), ["Return to the manifest menu."], "**Time cost:** 3 min", "Carrier POD cross-reference"),
        ("UNIT-LOCKER-MENU", obj(
            "The locker row smells like cold coffee and cleaning solution, mostly undisturbed.",
            "Several lockers are closed. One contractor locker door sits slightly open.",
            "The open locker door is not going to close itself while you decide.",
        ), ["Inspect the ajar contractor locker.", "Return to the break room."], "**Time cost:** 2 min", "Staff locker bank"),
        ("UNIT-LOCKER-SUCCESS", obj(
            "You ease the ajar door open and check past the folded coveralls inside.",
            "Inside the locker you find a contractor temporary badge that was not returned at exit.",
            "You note the badge and step back from the locker bank.",
        ), ["Return to the locker menu."], "**Time cost:** 3 min", "Locker inspect — success"),
        ("UNIT-LOCKER-FAIL", obj(
            "You ease the ajar door open and check what is inside.",
            "The locker interior looks unremarkable at a glance.",
            "Nothing stands out, so you step back from the locker bank.",
        ), ["Return to the locker menu."], "**Time cost:** 3 min", "Locker inspect — failure"),
        ("UNIT-DOCK-VIEW", obj(
            "You glance out the break room window toward the dock you just came from.",
            "Through the window you see the dock bay under sodium lights.",
            "You turn back into the room once you have seen enough.",
        ), ["Return to the break room."], "**Time cost:** 1 min", "Dock view from break room"),
    ]
    for uid, body, choices, meta, title in object_units:
        add(uid, "OBJECTS.md", body, choices, meta, title)

    check_flavor = {
        "UNIT-CHK-LATCH-DECL": ("Latch perception check", "You commit to a single careful look at the latch — there is no redoing this once you have decided."),
        "UNIT-CHK-LABEL-DECL": ("Label search check", "You commit to a close search of the aisle floor and pallet faces — one pass, no second look."),
        "UNIT-CHK-TREND-DECL": ("Trend export check", "You commit to running the export through the BMS menus — one attempt, and the interface will not be forgiving of a wrong click."),
        "UNIT-CHK-LOCKER-DECL": ("Locker perception check", "You commit to checking inside the ajar locker properly — one look, not a quick glance."),
    }
    for uid, (title, setup) in check_flavor.items():
        add(uid, "OBJECTS.md", f"{setup} Roll d20 plus your listed modifier once for this action.", ["Proceed to the success or failure section indicated by your roll."], "**Check:** one attempt", title)

    # ------------------------------------------------------------------
    # NPCs — scene context + quoted exchange, distinct voice per character.
    # Quoted lines are the original, approved dialogue and are unchanged.
    # ------------------------------------------------------------------

    def npc_body(scene: str, prompt: str, name: str, quote: str, coda: str = "") -> str:
        parts = [scene, f"*{prompt}*", f'**{name}** says: "{quote}"']
        if coda:
            parts.append(coda)
        return "\n\n".join(parts)

    npc_topic_times = _load_npc_topic_times()

    npc_entries = [
        ("UNIT-MARCUS-LATCH", npc_body(
            "Marcus stands by the security office's alarm panel, keys still hooked to his belt from rounds. He has already decided this conversation is about confirming he did his job correctly, and he answers like he is reading from a rounds log.",
            "Ask what you checked on the cold storage door during rounds.",
            "Marcus Hale",
            "I checked the cold storage latch at 11:00 p.m. It looked engaged.",
            "He taps the time into the air like it settles the matter.",
        )),
        ("UNIT-MARCUS-GAP", npc_body(
            "You raise the badge reader against his account, and Marcus's confidence flickers for the first time. He glances toward the archive terminal instead of you.",
            "Ask whether the badge reader log could differ from a latch check.",
            "Marcus Hale",
            "I had not pulled the badge reader log yet when the high-temperature alarm came in.",
            "It is not a confession — just an admission that his rounds and the record system never actually talked to each other tonight.",
        )),
        ("UNIT-MARCUS-ALARM", npc_body(
            "Back at the panel, Marcus points to a line of red text still sitting in the alarm history. This part he is sure of, because he watched it happen.",
            "Ask when the high-temperature alarm first appeared on your panel.",
            "Marcus Hale",
            "The high-temperature alarm hit my panel at 11:30 p.m. I called Elena right after.",
        )),
        ("UNIT-DEV-EXIT", npc_body(
            "Dev arrives at the dock still buttoning his coveralls, tool bag over one shoulder, clearly pulled out of bed by Elena's call. He answers fast, eager to account for his evening.",
            "Confirm when you left the site tonight.",
            "Dev Santos",
            "I scanned out at the dock a little after 7:00 p.m. CLO-1847 was done.",
        )),
        ("UNIT-DEV-CLO1847", npc_body(
            "He pulls up the closed ticket on his phone without being asked, like a contractor used to defending his own paperwork.",
            "Ask about CLO-1847 closeout details.",
            "Dev Santos",
            "CLO-1847 was legitimate CZ-1 maintenance. I closed the ticket on the engineering terminal.",
        )),
        ("UNIT-DEV-BADGE", npc_body(
            "This one costs him something. Dev rubs the back of his neck and will not quite meet your eyes.",
            "Press about whether your contractor badge left the building with you.",
            "Dev Santos",
            "I may have left my temporary badge in the break room locker.",
            "He says it like he is hoping you will tell him it does not matter.",
        )),
        ("UNIT-DEV-SESSION", npc_body(
            "By now he has stopped defending himself and started just answering — the kind of tired honesty that comes after you have already lost the argument with yourself.",
            "Ask whether any maintenance session was left active on CTRL-TERM-02.",
            "Dev Santos",
            "I did not log out of session SVC-REFRG-MAINT on CTRL-TERM-02. That was my mistake on closeout.",
        )),
        ("UNIT-LORI-DENY-COLD", npc_body(
            "Lori does not look up from the reconciliation screen when you come in. Her answer is immediate, flat, and clearly rehearsed before you even asked.",
            "Ask whether you entered cold storage after hours.",
            "Lori Okonkwo",
            "I did not go into cold storage tonight. Receiving work kept me at the desk.",
        )),
        ("UNIT-LORI-CONTROL-MIN", npc_body(
            "When you mention the control room, she finally looks at you — briefly — before turning back to her screen.",
            "Ask about your control room visit around 23:20.",
            "Lori Okonkwo",
            "I stepped into the control room briefly around 11:20 to check a screen message.",
            "She makes it sound smaller than a badge log will.",
        )),
        ("UNIT-LORI-PRESSURE", npc_body(
            "You lay the manifest exception in front of her. For a moment she just looks at the numbers, and the composed tone slips.",
            "Confront with manifest exception evidence from MNF-IN-4471.",
            "Lori Okonkwo",
            "MNF-IN-4471 does not match the carrier POD. I was trying to clear the exception before audit sampling.",
        )),
        ("UNIT-LORI-LABEL", npc_body(
            "The label residue is the thing she cannot argue with. Whatever composure she was holding onto finally goes.",
            "Press about label residue found in aisle C.",
            "Lori Okonkwo",
            "You found label residue. Receiving records and floor work in aisle C are connected. I did not expect the staging alarm to persist.",
            "It is the closest she comes to sounding sorry.",
        )),
        ("UNIT-ELENA-URGENCY", npc_body(
            "Elena has a phone in one hand and a clipboard in the other, and she answers you the way she has already answered three other people tonight — fast, without slowing down.",
            "Ask what operational steps you ordered after the alarm.",
            "Elena Morales",
            "After the 11:30 alarm I ordered staging checks and recalled Dev. Write-off planning starts if we cross 5:00 a.m.",
        )),
        ("UNIT-ELENA-STAFF", npc_body(
            "She takes a beat on this one, running the shift roster in her head before answering.",
            "Ask who was still on site working late.",
            "Elena Morales",
            "Lori was still reconciling manifests when I arrived. Marcus was on rounds. Pat's crew was on the dock.",
        )),
        ("UNIT-ELENA-RESTRICT", npc_body(
            "By now the dock has tape across two of the bay lanes, and Elena stands at the boundary like she is daring anyone to cross it without a reason.",
            "Ask about dock access restrictions.",
            "Elena Morales",
            "As of 3:15 a.m. dock access is restricted to essential movement until review finishes.",
        )),
        ("UNIT-PAT-DOOR", npc_body(
            "Pat is still pushing a mop cart when you catch them near the break room. They answer between sips of vending-machine coffee, like this is just another odd thing that happened on shift.",
            "Ask about unusual activity near the dock and cold hall.",
            "Pat Nguyen",
            "I propped the dock door for a cart around 11:40 p.m. I saw someone near the cold hall but not a face.",
        )),
        ("UNIT-PAT-SIL", npc_body(
            "You push for more, and Pat actually thinks about it instead of just shrugging you off — which tells you they are not hiding anything, there is just nothing more to find.",
            "Ask whether you could identify the person you saw.",
            "Pat Nguyen",
            "They moved like someone who knew the layout. I cannot name them.",
        )),
    ]
    for uid, body in npc_entries:
        add(
            uid,
            "NPCS.md",
            body,
            _topic_choices(uid),
            _topic_time_meta(uid, npc_topic_times),
            human_title(uid),
        )

    add(
        "UNIT-IT-ARCHIVE-POLICY",
        "NPCS.md",
        "A laminated notice is taped beside the archive terminal, the kind of card that outlives whoever posted it. It is signed only \"Records Desk — J. Reeves\" and reads like it was written for an audit, not for you.\n\n"
        "A records notice on the archive terminal explains that badge batch uploads complete on a fixed nightly schedule. The standard sync completes at 2:30 a.m.; full query fields unlock after sync.\n\n"
        "There is no one to argue with about it — the schedule runs whether you are waiting on it or not.",
        ["Return to the security office."],
        "**Records-only route | Time cost:** 2 min",
        "Archive sync policy notice",
    )
    mapping["SC-IT-RECORDS-POLICY"] = mapping["UNIT-IT-ARCHIVE-POLICY"].copy()
    mapping["SC-IT-RECORDS-POLICY"]["unit_id"] = "SC-IT-RECORDS-POLICY"

    # ------------------------------------------------------------------
    # Scenes — distinct revisit/transition prose per world-state variant.
    # ------------------------------------------------------------------

    scenes = {
        "SC-DOCK-ARRIVAL": (
            "Dock arrival briefing",
            "Elena walks you through the timeline at the briefing table: the 11:30 p.m. alarm, the staging checks she ordered, and the escort rule for the control room. She talks fast, the way people do when they have already explained something twice tonight and expect to explain it again.",
        ),
        "SC-DOCK-INITIAL-SURVEY": (
            "Initial dock survey",
            "Nothing is roped off yet. You walk the dock's open floor and note which corridors reach cold storage, the offices, and security — the layout you will be crossing back and forth all night.",
        ),
        "SC-SECURITY-ARCHIVE-OPEN": (
            "Archive sync complete",
            "The archive terminal chimes once, right on schedule, and the sync-pending banner clears. The full record set for tonight's badge activity is finally sitting there, waiting to be queried.",
        ),
        "SC-DOCK-RESTRICTED": (
            "Dock restriction active",
            "Tape now runs across two of the bay lanes, and Elena is enforcing it herself. Nonessential movement through the dock stops here until her review finishes.",
        ),
        "SC-SECURITY-UNSTAFFED": (
            "Security desk unstaffed",
            "Marcus's chair is empty — mandatory break, the schedule says — but the archive terminal is still logged in and the alarm panel keeps quietly doing its job without him.",
        ),
        "SC-ACCUSATION-PREP": (
            "Accountability preparation",
            "You spread your notes across the briefing table and start organizing them into a four-part accountability statement: who, how, what, and why. The clock does not stop while you write.",
        ),
        "SC-SECURITY-ARCHIVE-READY": (
            "Archive ready",
            "Every query field on the archive terminal is live now. Cold storage entries, control room entries, and the contractor's exit scan are all one selection away.",
        ),
        "SC-SECURITY-ARCHIVE-PENDING": (
            "Archive pending",
            "A small sync-in-progress icon sits over half the query menu. Some badge fields are grayed out entirely — the batch upload has not finished yet, and no amount of clicking speeds it up.",
        ),
        "SC-CONTROL-APPROACH": (
            "Control room approach",
            "The control room door has a badge reader you are not cleared to use on your own. Whether you get in now depends on whether Elena has already signed off on an escort.",
        ),
        "SC-CONTROL-CLEARED": (
            "Control room cleared",
            "The door unlocks without complaint. With escort clearance on record, the engineering workstations and staging panel are yours to work through under supervision.",
        ),
        "SC-CONTROL-ESCORT-REQUIRED": (
            "Escort required",
            "The reader blinks red. You will need to go back to the dock and have Elena sign the escort log before this door opens for you.",
        ),
        "SC-SECURITY-CROSSREF": (
            "Security cross-reference",
            "With a badge record finally in hand, you lay it next to the alarm history and start lining up timestamps side by side — door, badge, and alarm, all on the same clock.",
        ),
        "SC-COLD-AISLE-FOCUSED": (
            "Focused aisle revisit",
            "Now that you have seen the manifest gap, aisle C reads differently. You are not just walking the row anymore — you know roughly which pallet stack is worth a second, closer look.",
        ),
        "SC-COLD-LABEL-DETAIL": (
            "Label detail revisit",
            "With the recovered label backing already in your case file, you can go back and compare its print timestamp against pallet receipt records without searching from scratch again.",
        ),
        "SC-CONTROL-BMS-REVIEW": (
            "BMS review scene",
            "Having read the command log once, you can now set the staging suspension and the mute command's timing side by side and see how closely they line up.",
        ),
        "SC-MANAGER-PRESSURE-TOPIC": (
            "Manager interview pressure",
            "Physical trace from aisle C or the manifest exception itself gives you something concrete to put in front of Lori — and her answers change once you do.",
        ),
        "SC-BREAK-LOCKER-BRANCH": (
            "Optional locker branch",
            "The break room locker row is still available whenever you want it. Nothing about it expires, and nothing forces you to check it either.",
        ),
    }
    for sid, (title, body) in scenes.items():
        add(sid, "SCENES.md", body, ["Continue this scene thread.", "Return to the location base section for this area."], "**Scene transition**", title)

    # ------------------------------------------------------------------
    # Inference worksheets — record TYPES to consult, no answers revealed.
    # Questions and choice text are unchanged from the approved wording.
    # ------------------------------------------------------------------

    inf_data = {
        "INF-BADGE-MISATTRIBUTED": (
            "Does the cold-storage badge entry still implicate the contractor after comparing exit timing?",
            [
                "Cold storage inbound badge entry (security office archive)",
                "Contractor outbound dock scan (security office archive)",
                "Contractor's own account of the badge left behind (break room locker or interview)",
            ],
        ),
        "INF-STAGING-ROOT-CAUSE": (
            "Did staging suspension—not the door alarm alone—drive the sustained temperature rise?",
            [
                "BMS command log (control room workstation)",
                "CZ-1 staging indicator panel (control room)",
                "CZ-1 supply air temperature trend export (control room workstation)",
            ],
        ),
        "INF-RELABEL-FRAUD": (
            "Was pallet relabeling used to hide the inbound quantity short-ship?",
            [
                "Label adhesive residue and timestamp comparison (aisle C)",
                "Manifest MNF-IN-4471 versus carrier POD-4471 (manager office)",
                "Coordinator's account of the receiving exception (manager office interview)",
            ],
        ),
        "INF-CONTROL-ACCESS-MISMATCH": (
            "Who could issue the BMS mute command without refrigeration engineering privilege?",
            [
                "Control room door badge entry (security office archive)",
                "BMS command log and session identifier (control room workstation)",
            ],
        ),
        "INF-CULPRIT-SUPPORTED": (
            "Which role is supported by independent access, fraud, and control-room records?",
            [
                "Everything you have gathered on badge access, control room entry, and manifest fraud",
                "Cross-referenced timestamps from the security office",
            ],
        ),
        "INF-PERFECT-RECONSTRUCTION": (
            "Can you connect fraud concealment, unauthorized access, and staging suspension into one supported timeline?",
            [
                "Every record thread listed in the worksheets above",
                "The maintenance ticket and door-ajar alarm history (control room and security office)",
            ],
        ),
    }
    for iid, (q, record_types) in inf_data.items():
        record_list = "\n".join(f"- {r}" for r in record_types)
        body = (
            f"**Question:** {q}\n\n"
            f"**Record types to consult:**\n{record_list}\n\n"
            "Record the records you used. If synthesis fails, note which locations you will revisit."
        )
        add(iid, "INFERENCE.md", body, [
            "Mark synthesis complete if your answer is supported.",
            "Mark synthesis incomplete and follow a recovery prompt in the recovery file.",
        ], title=human_title(iid))

    # ------------------------------------------------------------------
    # Recovery routes — concrete location + action instructions.
    # ------------------------------------------------------------------

    rec_routes = {
        "REC-SECURITY-ARCHIVE": "Return to the security office and open the badge access archive terminal. From its query menu, run whichever badge record you have not pulled yet — cold storage entry, control room entry, or the contractor's outbound scan.",
        "REC-BREAK-LOCKER": "Head to the staff break room and walk the locker bank. If you have not already checked the contractor locker that sits ajar, do that now.",
        "REC-CONTROL-TERM": "Return to the automation control room and approach engineering workstation CTRL-TERM-02. Review whichever of the BMS command log, the closed maintenance ticket, or the temperature trend export you have not yet opened.",
        "REC-COLD-DISPLAY": "Go back into the cold storage hall and read the live CZ-1 supply air display. It costs almost no time and confirms what a trend export would otherwise show.",
        "REC-COLD-AISLE": "Return to the cold storage hall and walk the length of aisle C. Search the floor and pallet faces for label adhesive residue if you have not already.",
        "REC-MANAGER-MANIFEST": "Go to the warehouse manager office and compare manifest MNF-IN-4471 to the carrier delivery record at the receiving workstation.",
        "REC-MANAGER-INTERVIEW": "Go to the warehouse manager office and raise the receiving exception directly with Lori Okonkwo. Bring whatever manifest or physical evidence you already have — it changes how much she is willing to say.",
        "REC-SECURITY-CROSSREF": "Return to the security office and cross-reference the alarm history against the badge records you have already pulled. Line the timestamps up side by side.",
        "REC-REVISIT-ANY-UNRESOLVED-SOURCE": "Return to the loading dock and choose whichever location still has a record, a check, or a conversation you have not finished. A full reconstruction needs every thread accounted for.",
    }
    for rid, label in rec_routes.items():
        add(rid, "RECOVERY.md", label, ["Go to the named location and take the action described above."], title=human_title(rid))

    # ------------------------------------------------------------------
    # Endings — narrative consequence, spoiler policy preserved:
    # imperfect endings stay opaque about the culprit; only the fully
    # gated perfect ending names the full mechanism.
    # ------------------------------------------------------------------

    endings = {
        "END-PERFECT": (
            "Your accountability statement matches independent badge, manifest, physical, and BMS records. Compliance accepts a full reconstruction timeline: Lori Okonkwo borrowed Dev's forgotten badge to enter cold storage, swapped pallet labels to hide the short-ship, and used his unattended maintenance session to issue the mute command that suspended CZ-1 staging. "
            "Northline closes the shift with the write-off avoided and a documented case for both personnel review and the carrier dispute."
        ),
        "END-PARTIAL-INCOMPLETE": (
            "Compliance documents operational response gaps — the alarm history, supervisor actions, and temperature readings are on file, but several record threads never made it into your statement. "
            "Without a completed synthesis, the write-off review proceeds on the operational facts alone, and the question of exactly who caused tonight's failure stays open past your shift."
        ),
        "END-PARTIAL-WRONG-CULPRIT": (
            "Your statement centers on the contractor exit record, and Elena forwards it up the chain as filed. Dev's contract review gets flagged over a badge discrepancy he cannot fully explain away, even though the timeline you built does not quite hold together under scrutiny. "
            "Whatever actually reached into that unattended session on CTRL-TERM-02 goes unexamined tonight."
        ),
        "END-PARTIAL-TECH-ONLY": (
            "Your statement explains staging suspension and command timing in enough detail that engineering signs off on the mechanism. Compliance notes the unattended maintenance session as the technical root cause, with no name attached to who actually used it. "
            "The receiving floor's part in tonight's story never makes it into the record."
        ),
        "END-PARTIAL-MOTIVE-GAP": (
            "Receiving discrepancy records are noted in your statement, and the manifest exception on MNF-IN-4471 goes into the audit file as-is. The label residue and the relabeling it points to never quite connect into a finished synthesis. "
            "Someone will have to reopen the paperwork later to finish what your shift left half-drawn."
        ),
        "END-HIDDEN-RECORDS": (
            "You used the records-only archive policy route instead of pressing further into the operational alarm. IT's sync schedule goes into the audit trail exactly as documented — a routine 2:30 a.m. batch upload, nothing more. "
            "It is a clean footnote to file, but it does not answer why CZ-1 kept climbing after the alarm sounded."
        ),
        "END-NARRATIVE-CONTINUE": (
            "You defer final accountability while the clock still runs. Whatever you have learned so far stays open for revision from wherever you are standing in the facility. "
            "The night is not over, and neither is the investigation."
        ),
        "END-TIMEOUT": (
            "5:00 a.m. arrives before you finish. Compliance write-off procedures begin, and the health notification goes out on schedule regardless of what you found. "
            "Your investigation window closes under emergency protocol, whatever case you were building left unfinished."
        ),
    }
    for eid, body in endings.items():
        add(eid, "ENDINGS.md", body, title=human_title(eid))

    headers = {
        "LOCATIONS.md": "# Locations\n",
        "OBJECTS.md": "# Object interactions\n",
        "NPCS.md": "# People on site\n",
        "SCENES.md": "# Time and revisit scenes\n",
        "INFERENCE.md": "# Inference worksheets\n",
        "RECOVERY.md": "# Recovery routes\n",
        "ENDINGS.md": "# Endings\n\nOpen only the ending that matches your investigation outcome.\n",
    }
    for fname, parts in buckets.items():
        header = headers.get(fname, f"# {fname}\n")
        (PLAYER / fname).write_text(header + "\n".join(parts), encoding="utf-8")

    return mapping


def build_mapping_manifest(unit_map: dict[str, dict]) -> dict:
    return {
        "schema_version": "1.0",
        "adventure_id": "The_Cold_Storage_Alarm",
        "play_mode": "single_investigator",
        "unit_count": len(unit_map),
        "files": sorted({v["file"] for v in unit_map.values()}),
        "units": unit_map,
    }


def main() -> None:
    PLAYER.mkdir(parents=True, exist_ok=True)
    unit_map = write_player_files()
    manifest = build_mapping_manifest(unit_map)
    (ADV / "player_mapping_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {len(unit_map)} mapped units")


if __name__ == "__main__":
    main()
