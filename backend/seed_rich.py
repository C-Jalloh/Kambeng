"""
Rich seed script — populates all admin dashboard sections with realistic data.
Safe to re-run: skips records that already exist (checked by unique fields).
"""
import asyncio
import random
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, text

from app.db.database import AsyncSessionLocal
from app.core.security import get_password_hash

# Import every model so SQLAlchemy resolves all relationships
from app.models.user import User
from app.models.campaign import Campaign, CampaignMode, CampaignStatus
from app.models.campaign_goal import CampaignGoal  # noqa: F401
from app.models.campaign_update import CampaignUpdate  # noqa: F401
from app.models.update_attachment import UpdateAttachment  # noqa: F401
from app.models.donation import Donation
from app.models.payout import Payout
from app.models.proof import Proof  # noqa: F401
from app.models.review import Review  # noqa: F401
from app.models.kyc import KYC
from app.models.ledger import TransactionLedger, TransactionType, TransactionStatus
from app.models.audit_log import AdminAuditLog, AuditActionType
from app.models.alias import CampaignAlias  # noqa: F401
from app.models.moderation import ModerationReport, ReportEntityType, ReportReason, ReportStatus
from app.models.fraud_report import FraudReport  # noqa: F401
from app.models.fraud_report_notification_email import FraudReportNotificationEmail  # noqa: F401
from app.models.kyc_notification_email import KYCNotificationEmail  # noqa: F401
from app.models.recurring_donation import RecurringDonation  # noqa: F401


def ago(days: int, hours: int = 0) -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=days, hours=hours)


# ── 1. Users ──────────────────────────────────────────────────────────────────

USER_DEFS = [
    # (full_name, email, wave_number, role, is_active, kyc_status)
    ("Kambeng Admin",    "admin@kambeng.local",   "+2207000000", "ADMIN", True,  "NOT_SUBMITTED"),
    ("Awa Bah",          "awa@kambeng.local",     "+2207000001", "USER",  True,  "APPROVED"),
    ("Musa Jallow",      "musa@kambeng.local",    "+2207000002", "USER",  True,  "APPROVED"),
    ("Fatou Ceesay",     "fatou@kambeng.local",   "+2207000003", "USER",  True,  "APPROVED"),
    ("Omar Drammeh",     "omar@kambeng.local",    "+2207000004", "USER",  True,  "SUBMITTED"),
    ("Isatou Sanneh",    "isatou@kambeng.local",  "+2207000005", "USER",  True,  "REVIEWING"),
    ("Lamin Touray",     "lamin@kambeng.local",   "+2207000006", "USER",  True,  "REJECTED"),
    ("Binta Njie",       "binta@kambeng.local",   "+2207000007", "USER",  True,  "APPROVED"),
    ("Samba Faye",       "samba@kambeng.local",   "+2207000008", "USER",  False, "NOT_SUBMITTED"),
]


async def seed_users() -> dict[str, int]:
    ids: dict[str, int] = {}
    created = 0
    async with AsyncSessionLocal() as db:
        for full_name, email, wave, role, is_active, kyc_status in USER_DEFS:
            res = await db.execute(select(User).where(User.email == email))
            u = res.scalar_one_or_none()
            if u is None:
                u = User(
                    full_name=full_name, email=email, wave_number=wave,
                    password_hash=get_password_hash("StrongPass123!"),
                    role=role, is_active=is_active,
                    is_email_verified=True, kyc_status=kyc_status,
                )
                db.add(u)
                await db.flush()
                created += 1
            ids[email] = u.id
        await db.commit()
    print(f"Users: {created} created, {len(USER_DEFS) - created} existing")
    return ids


# ── 2. Campaigns ──────────────────────────────────────────────────────────────

CAMPAIGN_DEFS = [
    # (title, slug, description, mode, target, raised, status, owner_email)
    ("Books For Basse Schools",
     "books-for-basse-schools",
     "Fund books and classroom materials for students in Basse.",
     CampaignMode.TARGET, 50_000, 28_400, CampaignStatus.ACTIVE, "awa@kambeng.local"),

    ("Serrekunda Clinic Equipment",
     "serrekunda-clinic-equipment",
     "Raise funds to buy essential diagnostic tools for a community clinic.",
     CampaignMode.ONGOING, None, 15_200, CampaignStatus.ACTIVE, "musa@kambeng.local"),

    ("Kanifing Youth Football Club",
     "kanifing-youth-football",
     "Help young athletes get kits, boots, and training facilities.",
     CampaignMode.TARGET, 30_000, 30_000, CampaignStatus.CLOSED, "fatou@kambeng.local"),

    ("Bakau Clean Water Project",
     "bakau-clean-water",
     "Install water pumps and purification systems in Bakau.",
     CampaignMode.TARGET, 80_000, 12_750, CampaignStatus.ACTIVE, "binta@kambeng.local"),

    ("Orphanage Renovation Brikama",
     "orphanage-renovation-brikama",
     "Renovate dormitories and install solar power for the Brikama orphanage.",
     CampaignMode.ONGOING, None, 9_600, CampaignStatus.ACTIVE, "awa@kambeng.local"),

    ("Suspicious Fundraiser XYZ",
     "suspicious-fundraiser-xyz",
     "Unclear description with no verifiable goals.",
     CampaignMode.TARGET, 200_000, 1_500, CampaignStatus.SUSPENDED, "samba@kambeng.local"),
]


async def seed_campaigns(user_ids: dict[str, int]) -> dict[str, int]:
    ids: dict[str, int] = {}
    created = 0
    async with AsyncSessionLocal() as db:
        for title, slug, desc, mode, target, raised, status, owner_email in CAMPAIGN_DEFS:
            res = await db.execute(select(Campaign).where(Campaign.slug == slug))
            c = res.scalar_one_or_none()
            if c is None:
                c = Campaign(
                    user_id=user_ids[owner_email], title=title, slug=slug,
                    description=desc, mode=mode, target_amount=target,
                    amount_raised=raised, status=status,
                )
                db.add(c)
                await db.flush()
                created += 1
            ids[slug] = c.id
        await db.commit()
    print(f"Campaigns: {created} created, {len(CAMPAIGN_DEFS) - created} existing")
    return ids


# ── 3. Donations ──────────────────────────────────────────────────────────────

async def seed_donations(campaign_ids: dict[str, int]) -> None:
    SLUGS = list(campaign_ids.keys())

    succeeded = [
        # (ref, slug, amount, donor_name, days_ago, recon_source)
        ("DON-S001", "books-for-basse-schools",    500,  "Mariama Bah",     45, "webhook"),
        ("DON-S002", "books-for-basse-schools",   1200,  "Ebrima Jallow",   40, "webhook"),
        ("DON-S003", "serrekunda-clinic-equipment", 800, "Anonymous",        38, "webhook"),
        ("DON-S004", "kanifing-youth-football",    2500,  "Dawda Keita",     35, "webhook"),
        ("DON-S005", "books-for-basse-schools",    600,  "Rohey Njie",       30, "manual"),
        ("DON-S006", "bakau-clean-water",          3000,  "Lamin Ceesay",    28, "webhook"),
        ("DON-S007", "serrekunda-clinic-equipment",1500,  "Fatoumatta Saho", 22, "webhook"),
        ("DON-S008", "orphanage-renovation-brikama",750,  "Anonymous",       18, "manual"),
        ("DON-S009", "bakau-clean-water",          2000,  "Ousman Baldeh",   14, "webhook"),
        ("DON-S010", "books-for-basse-schools",    950,  "Amie Drammeh",    10, "webhook"),
        ("DON-S011", "serrekunda-clinic-equipment", 400, "Anonymous",         7, "webhook"),
        ("DON-S012", "orphanage-renovation-brikama",1800, "Sainey Camara",    5, "webhook"),
    ]

    pending_unreconciled = [
        # Awaiting manual admin reconciliation
        ("DON-P001", "bakau-clean-water",          1100, "Bakary Jatta",      3),
        ("DON-P002", "books-for-basse-schools",     700, "Anonymous",          2),
        ("DON-P003", "serrekunda-clinic-equipment", 500, "Haddy Saidy",        2),
        ("DON-P004", "orphanage-renovation-brikama",900, "Anonymous",          1),
        ("DON-P005", "bakau-clean-water",           450, "Binta Sonko",        1),
    ]

    created = 0
    async with AsyncSessionLocal() as db:
        # Succeeded donations
        for ref, slug, amount, donor, days, source in succeeded:
            res = await db.execute(select(Donation).where(Donation.client_reference == ref))
            if res.scalar_one_or_none() is None:
                db.add(Donation(
                    campaign_id=campaign_ids[slug],
                    client_reference=ref,
                    amount=float(amount),
                    status="SUCCEEDED",
                    donor_name=donor,
                    reconciliation_source=source,
                    created_at=ago(days),
                ))
                created += 1

        # Pending unreconciled (show on reconciliations page)
        for ref, slug, amount, donor, days in pending_unreconciled:
            res = await db.execute(select(Donation).where(Donation.client_reference == ref))
            if res.scalar_one_or_none() is None:
                db.add(Donation(
                    campaign_id=campaign_ids[slug],
                    client_reference=ref,
                    amount=float(amount),
                    status="PENDING",
                    donor_name=donor,
                    created_at=ago(days),
                ))
                created += 1

        await db.commit()
    print(f"Donations: {created} created")


# ── 4. Payouts ────────────────────────────────────────────────────────────────

async def seed_payouts(campaign_ids: dict[str, int]) -> None:
    PAYOUT_DEFS = [
        # (ref, slug, gross, hexai_fee, platform_commission, net, status, days_ago)
        ("OUT-001", "books-for-basse-schools",       10_000, 100, 10, 9_890,  "SUCCEEDED", 30),
        ("OUT-002", "serrekunda-clinic-equipment",    8_000,  80, 10, 7_910,  "SUCCEEDED", 20),
        ("OUT-003", "kanifing-youth-football",       25_000, 250, 10, 24_740, "SUCCEEDED", 15),
        ("OUT-004", "bakau-clean-water",              5_000,  50, 10, 4_940,  "SUCCEEDED", 10),
        ("OUT-005", "orphanage-renovation-brikama",   3_000,  30, 10, 2_960,  "SUCCEEDED",  6),
        ("OUT-006", "books-for-basse-schools",        7_500,  75, 10, 7_415,  "PENDING",    1),
    ]

    created = 0
    async with AsyncSessionLocal() as db:
        for ref, slug, gross, fee, comm, net, status, days in PAYOUT_DEFS:
            res = await db.execute(select(Payout).where(Payout.client_reference == ref))
            if res.scalar_one_or_none() is None:
                db.add(Payout(
                    campaign_id=campaign_ids[slug],
                    client_reference=ref,
                    gross_amount=float(gross),
                    hexai_fee=float(fee),
                    platform_commission=float(comm),
                    net_amount=float(net),
                    amount=float(net),
                    status=status,
                    created_at=ago(days),
                ))
                created += 1
        await db.commit()
    print(f"Payouts: {created} created")


# ── 5. KYC submissions ────────────────────────────────────────────────────────

async def seed_kyc(user_ids: dict[str, int], admin_id: int) -> None:
    KYC_DEFS = [
        # (email, doc_type, status, days_ago)
        ("omar@kambeng.local",   "NATIONAL_ID",     "SUBMITTED",  2),
        ("isatou@kambeng.local", "PASSPORT",        "REVIEWING",  5),
        ("lamin@kambeng.local",  "NATIONAL_ID",     "REJECTED",  30),
        ("binta@kambeng.local",  "DRIVERS_LICENSE", "APPROVED",  60),
        ("fatou@kambeng.local",  "PASSPORT",        "APPROVED",  90),
    ]

    created = 0
    async with AsyncSessionLocal() as db:
        for email, doc_type, status, days in KYC_DEFS:
            uid = user_ids[email]
            res = await db.execute(select(KYC).where(KYC.user_id == uid))
            if res.scalar_one_or_none() is None:
                k = KYC(
                    user_id=uid,
                    document_type=doc_type,
                    document_file_url=f"https://example.com/kyc/doc-{uid}.jpg",
                    status=status,
                    created_at=ago(days),
                )
                if status in ("APPROVED", "REJECTED"):
                    k.reviewed_by_admin_id = admin_id
                    k.reviewed_at = ago(days - 1)
                if status == "REJECTED":
                    k.rejection_reason = "Document is blurry or unreadable. Please resubmit a clearer photo."
                db.add(k)
                created += 1
        await db.commit()
    print(f"KYC submissions: {created} created")


# ── 6. Audit logs ─────────────────────────────────────────────────────────────

async def seed_audit_logs(user_ids: dict[str, int], campaign_ids: dict[str, int]) -> None:
    admin_id = user_ids["admin@kambeng.local"]
    camp_book = campaign_ids["books-for-basse-schools"]
    camp_susp = campaign_ids["suspicious-fundraiser-xyz"]

    AUDIT_DEFS = [
        # (action_type, entity_type, entity_id, description, days_ago)
        (AuditActionType.KYC_APPROVED, "KYC", user_ids["binta@kambeng.local"],
         "KYC submission approved for Binta Njie", 59),
        (AuditActionType.KYC_APPROVED, "KYC", user_ids["fatou@kambeng.local"],
         "KYC submission approved for Fatou Ceesay", 89),
        (AuditActionType.KYC_REJECTED, "KYC", user_ids["lamin@kambeng.local"],
         "KYC rejected — document unreadable (Lamin Touray)", 29),
        (AuditActionType.CAMPAIGN_SUSPENDED, "Campaign", camp_susp,
         "Campaign 'Suspicious Fundraiser XYZ' suspended pending fraud investigation", 10),
        (AuditActionType.DONATION_MANUAL_APPROVED, "Donation", 1,
         "Manual donation reconciliation approved — DON-S005", 30),
        (AuditActionType.DONATION_MANUAL_APPROVED, "Donation", 2,
         "Manual donation reconciliation approved — DON-S008", 18),
        (AuditActionType.USER_DISABLED, "User", user_ids["samba@kambeng.local"],
         "User Samba Faye disabled pending fraud review", 9),
        (AuditActionType.COMMISSION_WITHDRAWAL_INITIATED, "Payout", 1,
         "Platform commission withdrawal initiated — 10 GMD", 6),
        (AuditActionType.COMMISSIONS_VIEWED, "Payout", 0,
         "Admin viewed commissions summary. Available: 60.0", 1),
        (AuditActionType.PAYOUT_MANUAL_OVERRIDE, "Payout", 6,
         "Payout OUT-006 manually set to PENDING override", 1),
        (AuditActionType.CAMPAIGN_REACTIVATED, "Campaign", camp_book,
         "Campaign 'Books For Basse Schools' reactivated after review", 5),
        (AuditActionType.USER_ENABLED, "User", user_ids["awa@kambeng.local"],
         "User Awa Bah re-enabled after identity verification", 4),
    ]

    created = 0
    async with AsyncSessionLocal() as db:
        for action, entity_type, entity_id, desc, days in AUDIT_DEFS:
            log = AdminAuditLog(
                action_type=action.value,
                performed_by_admin_id=admin_id,
                target_entity_type=entity_type,
                target_entity_id=entity_id,
                description=desc,
                created_at=ago(days),
            )
            db.add(log)
            created += 1
        await db.commit()
    print(f"Audit logs: {created} created")


# ── 7. Moderation reports ─────────────────────────────────────────────────────

async def seed_moderation(user_ids: dict[str, int], campaign_ids: dict[str, int]) -> None:
    admin_id = user_ids["admin@kambeng.local"]
    camp_susp = campaign_ids["suspicious-fundraiser-xyz"]
    camp_book = campaign_ids["books-for-basse-schools"]
    camp_water = campaign_ids["bakau-clean-water"]

    REPORT_DEFS = [
        # (entity_type_str, entity_id, reporter_email, reason_str, description, status_str, days_ago)
        ("CAMPAIGN", camp_susp,
         "awa@kambeng.local", "SCAM",
         "This campaign has no verifiable goals and the organiser cannot be reached.",
         "REVIEWING", 12),

        ("CAMPAIGN", camp_susp,
         "musa@kambeng.local", "FALSE_INFORMATION",
         "The campaign claims government backing but there is no supporting evidence.",
         "OPEN", 10),

        ("CAMPAIGN", camp_book,
         "fatou@kambeng.local", "SPAM",
         "This campaign is being shared aggressively and feels like spam.",
         "RESOLVED", 25),

        ("USER", user_ids["samba@kambeng.local"],
         "binta@kambeng.local", "SCAM",
         "This user tried to solicit donations outside the platform via WhatsApp.",
         "RESOLVED", 11),

        ("CAMPAIGN", camp_water,
         "lamin@kambeng.local", "INAPPROPRIATE_CONTENT",
         "Campaign description contains an offensive photo in the gallery.",
         "OPEN", 3),

        ("REVIEW", 1,
         None, "HARASSMENT",
         "A review on this campaign contains targeted harassment against the organiser.",
         "OPEN", 1),
    ]

    created = 0
    async with AsyncSessionLocal() as db:
        for entity_type, entity_id, reporter_email, reason, desc, status, days in REPORT_DEFS:
            resolved_by = admin_id if status in ("RESOLVED", "DISMISSED") else None
            resolved_at = ago(days - 1) if status in ("RESOLVED", "DISMISSED") else None
            note = "Reviewed and resolved by admin." if status in ("RESOLVED", "DISMISSED") else None
            camp_id = entity_id if entity_type == "CAMPAIGN" else None
            reporter_id = user_ids[reporter_email] if reporter_email else None
            # Use raw SQL to avoid SQLAlchemy casting to the non-existent native enum type
            await db.execute(text("""
                INSERT INTO moderation_reports
                  (reported_entity_type, reported_entity_id, campaign_id,
                   reported_by_user_id, reason, description, status,
                   moderation_note, resolved_by_admin_id, resolved_at, created_at, updated_at)
                VALUES
                  (:et, :eid, :cid, :rid, :reason, :desc, :status,
                   :note, :res_by, :res_at, :created_at, :created_at)
            """), {
                "et": entity_type, "eid": entity_id, "cid": camp_id,
                "rid": reporter_id, "reason": reason, "desc": desc, "status": status,
                "note": note, "res_by": resolved_by, "res_at": resolved_at,
                "created_at": ago(days),
            })
            created += 1
        await db.commit()
    print(f"Moderation reports: {created} created")


# ── 8. Transaction ledger ─────────────────────────────────────────────────────

async def seed_ledger(campaign_ids: dict[str, int], user_ids: dict[str, int]) -> None:
    admin_id = user_ids["admin@kambeng.local"]

    LEDGER_DEFS = [
        # (campaign_slug, tx_type, status, gross, hexai_fee, comm, net, ref, days_ago)
        ("books-for-basse-schools",       TransactionType.DONATION,    TransactionStatus.SUCCEEDED, 500,    5,   0,   495,  "DON-S001", 45),
        ("books-for-basse-schools",       TransactionType.DONATION,    TransactionStatus.SUCCEEDED, 1200,  12,   0,  1188,  "DON-S002", 40),
        ("serrekunda-clinic-equipment",   TransactionType.DONATION,    TransactionStatus.SUCCEEDED, 800,    8,   0,   792,  "DON-S003", 38),
        ("kanifing-youth-football",       TransactionType.DONATION,    TransactionStatus.SUCCEEDED, 2500,  25,   0,  2475,  "DON-S004", 35),
        ("bakau-clean-water",             TransactionType.DONATION,    TransactionStatus.SUCCEEDED, 3000,  30,   0,  2970,  "DON-S006", 28),
        ("serrekunda-clinic-equipment",   TransactionType.DONATION,    TransactionStatus.SUCCEEDED, 1500,  15,   0,  1485,  "DON-S007", 22),
        ("bakau-clean-water",             TransactionType.DONATION,    TransactionStatus.SUCCEEDED, 2000,  20,   0,  1980,  "DON-S009", 14),

        ("books-for-basse-schools",       TransactionType.WITHDRAWAL,  TransactionStatus.SUCCEEDED, 10000, 100, 10,  9890,  "OUT-001",  30),
        ("serrekunda-clinic-equipment",   TransactionType.WITHDRAWAL,  TransactionStatus.SUCCEEDED, 8000,   80, 10,  7910,  "OUT-002",  20),
        ("kanifing-youth-football",       TransactionType.WITHDRAWAL,  TransactionStatus.SUCCEEDED, 25000, 250, 10, 24740,  "OUT-003",  15),
        ("bakau-clean-water",             TransactionType.WITHDRAWAL,  TransactionStatus.SUCCEEDED, 5000,   50, 10,  4940,  "OUT-004",  10),
        ("orphanage-renovation-brikama",  TransactionType.WITHDRAWAL,  TransactionStatus.SUCCEEDED, 3000,   30, 10,  2960,  "OUT-005",   6),

        ("books-for-basse-schools",       TransactionType.FEE_PLATFORM, TransactionStatus.SUCCEEDED, 10,   0,   0,    10,  "FEE-001",  30),
        ("serrekunda-clinic-equipment",   TransactionType.FEE_PLATFORM, TransactionStatus.SUCCEEDED, 10,   0,   0,    10,  "FEE-002",  20),
        ("kanifing-youth-football",       TransactionType.FEE_PLATFORM, TransactionStatus.SUCCEEDED, 10,   0,   0,    10,  "FEE-003",  15),
    ]

    created = 0
    async with AsyncSessionLocal() as db:
        for slug, tx_type, status, gross, fee, comm, net, ref, days in LEDGER_DEFS:
            res = await db.execute(
                select(TransactionLedger).where(TransactionLedger.external_reference == ref)
            )
            if res.scalar_one_or_none() is None:
                db.add(TransactionLedger(
                    campaign_id=campaign_ids[slug],
                    transaction_type=tx_type.value,
                    status=status.value,
                    gross_amount=float(gross),
                    hexai_fee=float(fee),
                    platform_commission=float(comm),
                    net_amount=float(net),
                    external_reference=ref,
                    created_by_user_id=admin_id,
                    created_at=ago(days),
                ))
                created += 1
        await db.commit()
    print(f"Ledger entries: {created} created")


# ── Main ──────────────────────────────────────────────────────────────────────

async def main() -> None:
    print("=== Rich seed starting ===")
    user_ids = await seed_users()
    campaign_ids = await seed_campaigns(user_ids)
    await seed_donations(campaign_ids)
    await seed_payouts(campaign_ids)
    await seed_kyc(user_ids, admin_id=user_ids["admin@kambeng.local"])
    await seed_audit_logs(user_ids, campaign_ids)
    await seed_moderation(user_ids, campaign_ids)
    await seed_ledger(campaign_ids, user_ids)
    print("\n=== Seed complete ===")
    print("Admin login:  +2207000000  /  StrongPass123!")
    print("User login:   +2207000001  /  StrongPass123!")


if __name__ == "__main__":
    asyncio.run(main())
