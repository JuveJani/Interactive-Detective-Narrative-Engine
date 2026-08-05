#!/usr/bin/env python3
"""Generate PLAYER markdown and mapping manifest for The Cold Storage Alarm."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADV = ROOT / "adventures" / "The_Cold_Storage_Alarm"
ADVENTURE = ADV / "adventure"
PLAYER = ADVENTURE / "PLAYER"


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

    def add(uid: str, fname: str, body: str, choices: list[str] | None = None, meta: str = "", title: str | None = None) -> None:
        block = unit_block(uid, body, choices, meta, title)
        buckets.setdefault(fname, []).append(block)
        mapping[uid] = {"file": f"PLAYER/{fname}", "anchor": title or human_title(uid), "unit_id": uid}

    buckets: dict[str, list[str]] = {}

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

Start with the opening section, then `HOW_TO_PLAY.md`. Follow section prompts in order; do not read ahead in ending sections.
""",
        encoding="utf-8",
    )

    (PLAYER / "NAVIGATION_INDEX.md").write_text(
        """# Navigation index

Do not read ahead in these files.

- Opening briefing uses the opening file.
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

    add("UNIT-DOCK-BASE", "LOCATIONS.md", "The loading dock is lit by sodium fixtures. Forklifts sit idle. Elena Morales watches the bay doors while staff move between the dock and the office wing.", [
        "Walk through the dock corridor to the cold storage hall.",
        "Head inside to the staff break room.",
        "Cut through the warehouse corridor to the security office.",
        "Take the office wing corridor to the warehouse manager office.",
        "Review the supervisor briefing area.",
        "Request escort clearance to the automation control room.",
    ], "**Location:** Loading dock | **Time cost:** 0 min", "Loading dock")

    add("UNIT-COLD-BASE", "LOCATIONS.md", "Cold air rolls from the hall doors. Pallet rows stretch toward zone CZ-1.", [
        "Examine the cold storage door latch and reader.",
        "Walk the length of aisle C between the pallet rows.",
        "Read the live CZ-1 supply air temperature display.",
        "Follow the engineering passage to the automation control room.",
        "Return to the loading dock.",
        "Return toward the break room corridor.",
    ], "**Location:** Cold storage hall | **Time cost:** 0 min", "Cold storage hall")

    add("UNIT-CONTROL-BASE", "LOCATIONS.md", "The automation control room holds engineering workstations and a CZ-1 staging indicator panel.", [
        "Approach the engineering workstation.",
        "Inspect the CZ-1 staging indicator panel.",
        "Return to the cold storage hall.",
        "Return to the loading dock with the supervisor.",
        "Return to the security office.",
    ], "**Location:** Automation control room | **Time cost:** 0 min", "Automation control room")

    add("UNIT-SECURITY-BASE", "LOCATIONS.md", "The security office holds an alarm panel and a badge archive terminal.", [
        "Review recent alarm history on the security panel.",
        "Open the badge access archive terminal.",
        "Return to the loading dock.",
        "Return to the break room.",
    ], "**Location:** Security office | **Time cost:** 0 min", "Security office")

    add("UNIT-MANAGER-BASE", "LOCATIONS.md", "The warehouse manager office is open for the emergency. Lori Okonkwo's receiving workstation still shows an active reconciliation screen.", [
        "Review the open receiving reconciliation screen.",
        "Speak with Lori Okonkwo about receiving and access topics you have unlocked.",
        "Return to the loading dock.",
        "Return to the break room.",
    ], "**Location:** Warehouse manager office | **Time cost:** 0 min", "Warehouse manager office")

    add("UNIT-BREAK-BASE", "LOCATIONS.md", "The staff break room has vending machines, lockers, and a window toward the dock.", [
        "Walk along the staff locker bank.",
        "Look out toward the dock loading area.",
        "Return to the loading dock.",
        "Walk to the manager office through the staff corridor.",
        "Follow the interior hallway to the security office.",
        "Take the side passage toward the cold storage hall.",
    ], "**Location:** Staff break room | **Time cost:** 0 min", "Staff break room")

    object_units = [
        ("UNIT-DOCK-BRIEFING-MENU", "Elena points to a printed incident timeline on the briefing table.", ["Return to the loading dock."], "**Time cost:** 2 min", "Supervisor briefing"),
        ("UNIT-ESCORT-GRANTED", "Elena signs an escort log and walks you toward the engineering passage.", ["Return to the loading dock."], "**Time cost:** 3 min", "Escort granted"),
        ("UNIT-COLD-DOOR-MENU", "The cold storage door has a badge reader and a heavy latch.", ["Check the latch hardware for recent disturbance.", "Return to the cold storage hall."], "**Time cost:** 3 min", "Cold storage door"),
        ("UNIT-LATCH-SUCCESS", "Under the latch plate you notice fresh scuffing where hardware was recently handled.", ["Return to the cold storage door menu."], "**Time cost:** 4 min", "Latch check — success"),
        ("UNIT-LATCH-FAIL", "The latch hardware looks ordinary from this angle; nothing useful stands out.", ["Return to the cold storage door menu."], "**Time cost:** 4 min", "Latch check — failure"),
        ("UNIT-AISLE-C-MENU", "Aisle C runs between high pallet rows.", ["Search the floor and pallet faces for label adhesive residue.", "Return to the cold storage hall."], "**Time cost:** 2 min", "Aisle C"),
        ("UNIT-LABEL-SUCCESS", "You recover a strip of label backing with fresh adhesive trace.", ["Return to aisle C menu."], "**Time cost:** 5 min", "Label search — success"),
        ("UNIT-LABEL-FAIL", "The floor and pallet faces show routine warehouse wear; no distinctive trace stands out.", ["Return to aisle C menu."], "**Time cost:** 5 min", "Label search — failure"),
        ("UNIT-LABEL-DETAIL", "You compare the recovered backing print timestamp to pallet receipt records. The timestamp does not match the original partial-pallet location.", ["Return to aisle C menu."], "**Time cost:** 4 min", "Label timestamp comparison"),
        ("UNIT-TEMP-LIVE", "The live display reads CZ-1 supply air at a sustained rise above the cold-chain threshold.", ["Return to the cold storage hall."], "**Time cost:** 1 min", "Live temperature display"),
        ("UNIT-TERM-02-MENU", "Engineering workstation CTRL-TERM-02 is awake.", [
            "Review the BMS command log on this terminal.",
            "Open the closed maintenance ticket for CZ-1.",
            "Export the CZ-1 supply air temperature trend.",
            "Return to the control room.",
        ], "**Time cost:** 1 min", "Engineering workstation"),
        ("UNIT-BMS-COMMAND", "The command log shows CMD-CZ1-MUTE-STAGE issued at 11:22 p.m. under maintenance session SVC-REFRG-MAINT.", ["Return to the engineering workstation menu."], "**Time cost:** 4 min", "BMS command log"),
        ("UNIT-MAINT-TICKET", "Ticket CLO-1847 closed at 6:30 p.m. with a note that session SVC-REFRG-MAINT was left unlocked.", ["Return to the engineering workstation menu."], "**Time cost:** 3 min", "Maintenance ticket"),
        ("UNIT-TREND-SUCCESS", "The trend export completes. Supply air inflects upward after 11:27 p.m.", ["Return to the engineering workstation menu."], "**Time cost:** 5 min", "Trend export — success"),
        ("UNIT-TREND-FAIL", "The export wizard closes with an error; no trend file is saved.", ["Return to the engineering workstation menu."], "**Time cost:** 5 min", "Trend export — failure"),
        ("UNIT-STAGING-PANEL", "The CZ-1 staging panel shows compressor staging suspended.", ["Return to the control room."], "**Time cost:** 3 min", "Staging indicator panel"),
        ("UNIT-ALARM-HISTORY", "Alarm history lists ALM-COLD-DOOR-AJAR at 11:18 p.m. and ALM-COLD-HIGH at 11:30 p.m.", ["Return to the security office."], "**Time cost:** 3 min", "Alarm history"),
        ("UNIT-BADGE-ARCHIVE-MENU", "The badge archive terminal shows whether tonight's batch upload has finished.", [
            "Query cold storage inbound badge entries for tonight.",
            "Query control room door entries for tonight.",
            "Pull the contractor outbound dock scan record.",
            "Return to the security office.",
        ], "**Time cost:** 2 min", "Badge archive terminal"),
        ("UNIT-BADGE-COLD-ENTRY", "Cold storage inbound log shows credential BADGE-DEV-TEMP at 11:14 p.m.", ["Return to the badge archive menu."], "**Time cost:** 4 min", "Cold storage badge query"),
        ("UNIT-BADGE-CONTROL-ENTRY", "Control room entry log shows badge BADGE-LORI at 11:20 p.m.", ["Return to the badge archive menu."], "**Time cost:** 3 min", "Control room badge query"),
        ("UNIT-EXIT-SCAN", "Outbound dock scan shows Dev Santos exited at 7:02 p.m.", ["Return to the badge archive menu."], "**Time cost:** 3 min", "Contractor exit scan"),
        ("UNIT-MANIFEST-MENU", "The receiving screen still flags manifest MNF-IN-4471.", [
            "Compare manifest MNF-IN-4471 to the carrier delivery record.",
            "Cross-reference the signed carrier POD against bay assignments.",
            "Return to the manager office.",
        ], "**Time cost:** 2 min", "Receiving workstation"),
        ("UNIT-MANIFEST-GAP", "Manifest MNF-IN-4471 shows eight cases received while carrier POD-4471 lists forty-eight.", ["Return to the manifest menu."], "**Time cost:** 5 min", "Manifest comparison"),
        ("UNIT-POD-CROSSREF", "The signed POD assigns the full shipment to bay C3 expecting a complete lot scan.", ["Return to the manifest menu."], "**Time cost:** 3 min", "Carrier POD cross-reference"),
        ("UNIT-LOCKER-MENU", "Several lockers are closed. One contractor locker door sits slightly open.", ["Inspect the ajar contractor locker.", "Return to the break room."], "**Time cost:** 2 min", "Staff locker bank"),
        ("UNIT-LOCKER-SUCCESS", "Inside the locker you find a contractor temporary badge that was not returned at exit.", ["Return to the locker menu."], "**Time cost:** 3 min", "Locker inspect — success"),
        ("UNIT-LOCKER-FAIL", "The locker interior looks unremarkable at a glance.", ["Return to the locker menu."], "**Time cost:** 3 min", "Locker inspect — failure"),
        ("UNIT-DOCK-VIEW", "Through the window you see the dock bay under sodium lights.", ["Return to the break room."], "**Time cost:** 1 min", "Dock view from break room"),
    ]
    for uid, body, choices, meta, title in object_units:
        add(uid, "OBJECTS.md", body, choices, meta, title)

    for uid, title in [
        ("UNIT-CHK-LATCH-DECL", "Latch perception check"),
        ("UNIT-CHK-LABEL-DECL", "Label search check"),
        ("UNIT-CHK-TREND-DECL", "Trend export check"),
        ("UNIT-CHK-LOCKER-DECL", "Locker perception check"),
    ]:
        add(uid, "OBJECTS.md", "Roll d20 plus your listed modifier once for this action.", ["Proceed to the success or failure section indicated by your roll."], "**Check:** one attempt", title)

    npc_lines = {
        "UNIT-MARCUS-LATCH": ("Marcus Hale", "I checked the cold storage latch at 11:00 p.m. It looked engaged."),
        "UNIT-MARCUS-GAP": ("Marcus Hale", "I had not pulled the badge reader log yet when the high-temperature alarm came in."),
        "UNIT-MARCUS-ALARM": ("Marcus Hale", "The high-temperature alarm hit my panel at 11:30 p.m. I called Elena right after."),
        "UNIT-DEV-EXIT": ("Dev Santos", "I scanned out at the dock a little after 7:00 p.m. CLO-1847 was done."),
        "UNIT-DEV-CLO1847": ("Dev Santos", "CLO-1847 was legitimate CZ-1 maintenance. I closed the ticket on the engineering terminal."),
        "UNIT-DEV-BADGE": ("Dev Santos", "I may have left my temporary badge in the break room locker."),
        "UNIT-DEV-SESSION": ("Dev Santos", "I did not log out of session SVC-REFRG-MAINT on CTRL-TERM-02. That was my mistake on closeout."),
        "UNIT-LORI-DENY-COLD": ("Lori Okonkwo", "I did not go into cold storage tonight. Receiving work kept me at the desk."),
        "UNIT-LORI-CONTROL-MIN": ("Lori Okonkwo", "I stepped into the control room briefly around 11:20 to check a screen message."),
        "UNIT-LORI-PRESSURE": ("Lori Okonkwo", "MNF-IN-4471 does not match the carrier POD. I was trying to clear the exception before audit sampling."),
        "UNIT-LORI-LABEL": ("Lori Okonkwo", "You found label residue. Receiving records and floor work in aisle C are connected. I did not expect the staging alarm to persist."),
        "UNIT-ELENA-URGENCY": ("Elena Morales", "After the 11:30 alarm I ordered staging checks and recalled Dev. Write-off planning starts if we cross 5:00 a.m."),
        "UNIT-ELENA-STAFF": ("Elena Morales", "Lori was still reconciling manifests when I arrived. Marcus was on rounds. Pat's crew was on the dock."),
        "UNIT-ELENA-RESTRICT": ("Elena Morales", "As of 3:15 a.m. dock access is restricted to essential movement until review finishes."),
        "UNIT-PAT-DOOR": ("Pat Nguyen", "I propped the dock door for a cart around 11:40 p.m. I saw someone near the cold hall but not a face."),
        "UNIT-PAT-SIL": ("Pat Nguyen", "They moved like someone who knew the layout. I cannot name them."),
    }
    for uid, (name, line) in npc_lines.items():
        add(uid, "NPCS.md", f'**{name}** says: "{line}"', ["Return to your current location menu or continue the conversation."], "**Time cost:** varies by topic", human_title(uid))

    add("UNIT-IT-ARCHIVE-POLICY", "NPCS.md", "A records notice on the archive terminal explains that badge batch uploads complete on a fixed nightly schedule. The standard sync completes at 2:30 a.m.; full query fields unlock after sync.", ["Return to the security office."], "**Records-only route | Time cost:** 2 min", "Archive sync policy notice")
    mapping["SC-IT-RECORDS-POLICY"] = mapping["UNIT-IT-ARCHIVE-POLICY"].copy()
    mapping["SC-IT-RECORDS-POLICY"]["unit_id"] = "SC-IT-RECORDS-POLICY"

    scenes = {
        "SC-DOCK-ARRIVAL": ("Dock arrival briefing", "Elena summarizes the alarm timeline and your escort rules."),
        "SC-DOCK-INITIAL-SURVEY": ("Initial dock survey", "You note which corridors reach cold storage, offices, and security."),
        "SC-SECURITY-ARCHIVE-OPEN": ("Archive sync complete", "The archive terminal now shows full query fields for tonight."),
        "SC-DOCK-RESTRICTED": ("Dock restriction active", "Elena limits nonessential dock movement while review continues."),
        "SC-SECURITY-UNSTAFFED": ("Security desk unstaffed", "Marcus is on break. The archive terminal remains powered."),
        "SC-ACCUSATION-PREP": ("Accountability preparation", "You organize records for a four-part accountability statement."),
        "SC-SECURITY-ARCHIVE-READY": ("Archive ready", "Badge archive sync finished; cold and control queries are enabled."),
        "SC-SECURITY-ARCHIVE-PENDING": ("Archive pending", "Some badge fields remain queued until sync completes."),
        "SC-CONTROL-APPROACH": ("Control room approach", "Escort clearance may be required."),
        "SC-CONTROL-CLEARED": ("Control room cleared", "Engineering workstations are available under supervision."),
        "SC-CONTROL-ESCORT-REQUIRED": ("Escort required", "Request clearance from Elena at the dock briefing area."),
        "SC-SECURITY-CROSSREF": ("Security cross-reference", "You compare door, badge, and alarm timestamps side by side."),
        "SC-COLD-AISLE-FOCUSED": ("Focused aisle revisit", "Manifest gap notes suggest which pallet row deserves closer inspection."),
        "SC-COLD-LABEL-DETAIL": ("Label detail revisit", "You can compare backing timestamps in aisle C."),
        "SC-CONTROL-BMS-REVIEW": ("BMS review scene", "Staging suspension and command timing can be read together."),
        "SC-MANAGER-PRESSURE-TOPIC": ("Manager interview pressure", "Physical trace or manifest records may unlock further dialogue."),
        "SC-BREAK-LOCKER-BRANCH": ("Optional locker branch", "The break room locker row is available if you choose to visit."),
    }
    for sid, (title, body) in scenes.items():
        add(sid, "SCENES.md", body, ["Continue this scene thread.", "Return to the location base section for this area."], "**Scene transition**", title)

    inf_q = {
        "INF-BADGE-MISATTRIBUTED": "Does the cold-storage badge entry still implicate the contractor after comparing exit timing?",
        "INF-STAGING-ROOT-CAUSE": "Did staging suspension—not the door alarm alone—drive the sustained temperature rise?",
        "INF-RELABEL-FRAUD": "Was pallet relabeling used to hide the inbound quantity short-ship?",
        "INF-CONTROL-ACCESS-MISMATCH": "Who could issue the BMS mute command without refrigeration engineering privilege?",
        "INF-CULPRIT-SUPPORTED": "Which role is supported by independent access, fraud, and control-room records?",
        "INF-PERFECT-RECONSTRUCTION": "Can you connect fraud concealment, unauthorized access, and staging suspension into one supported timeline?",
    }
    for iid, q in inf_q.items():
        add(uid, "INFERENCE.md", f"**Question:** {q}\n\nRecord the records you used. If synthesis fails, note which locations you will revisit.", [
            "Mark synthesis complete if your answer is supported.",
            "Mark synthesis incomplete and follow a recovery prompt in the recovery file.",
        ], title=human_title(iid))

    rec_routes = {
        "REC-SECURITY-ARCHIVE": "Return to the security office badge archive terminal.",
        "REC-BREAK-LOCKER": "Inspect the staff locker bank in the break room.",
        "REC-CONTROL-TERM": "Review the engineering workstation in the control room.",
        "REC-COLD-DISPLAY": "Read the live CZ-1 supply air display in the cold hall.",
        "REC-COLD-AISLE": "Search aisle C for label residue.",
        "REC-MANAGER-MANIFEST": "Compare manifest MNF-IN-4471 at the manager workstation.",
        "REC-MANAGER-INTERVIEW": "Speak with the logistics coordinator in the manager office.",
        "REC-SECURITY-CROSSREF": "Cross-reference badge and alarm records at security.",
        "REC-REVISIT-ANY-UNRESOLVED-SOURCE": "Revisit any location where review remains incomplete.",
    }
    for rid, label in rec_routes.items():
        add(rid, "RECOVERY.md", f"When an inference step fails, you may: {label}", ["Go to the linked location base section and perform the action."], title=human_title(rid))

    endings = {
        "END-PERFECT": "Your accountability statement matches independent badge, manifest, physical, and BMS records. Compliance accepts a full reconstruction timeline.",
        "END-PARTIAL-INCOMPLETE": "Compliance documents operational response gaps. Several record threads remain unresolved in your statement.",
        "END-PARTIAL-WRONG-CULPRIT": "Your statement centers on the contractor exit record. Later badge and access records do not fully support that assignment.",
        "END-PARTIAL-TECH-ONLY": "Your statement explains staging suspension and command timing but does not connect receiving discrepancies.",
        "END-PARTIAL-MOTIVE-GAP": "Receiving discrepancy records are noted, but relabeling synthesis is incomplete.",
        "END-HIDDEN-RECORDS": "You used the records-only archive policy route. IT sync timing is documented for audit without resolving the operational alarm alone.",
        "END-NARRATIVE-CONTINUE": "You defer final accountability while the clock still runs. Continue investigating from your current location base section.",
        "END-TIMEOUT": "5:00 a.m. arrives. Compliance write-off procedures begin. Your investigation window closes under emergency protocol.",
    }
    for eid, body in endings.items():
        add(eid, "ENDINGS.md", body, title=human_title(eid))

    for fname, parts in buckets.items():
        header = {"LOCATIONS.md": "# Locations\n", "OBJECTS.md": "# Object interactions\n", "NPCS.md": "# People on site\n", "SCENES.md": "# Time and revisit scenes\n", "INFERENCE.md": "# Inference worksheets\n", "RECOVERY.md": "# Recovery routes\n", "ENDINGS.md": "# Endings\n\nOpen only the ending that matches your investigation outcome.\n"}.get(fname, f"# {fname}\n")
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
