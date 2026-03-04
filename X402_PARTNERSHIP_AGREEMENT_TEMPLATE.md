# x402 Partnership Agreement
## Regime Classifier API × x402 Payment Facilitator

**THIS IS A TEMPLATE.** Please have a lawyer review before signing.

---

## 1. PARTIES

This Agreement is entered into as of the date signed below ("Effective Date") between:

- **Sentinel Algorithms LLC**, a [State] limited liability company ("Sentinel"), and
- **[Partner Legal Entity Name]**, a [State/Country] [legal structure] ("Partner")

---

## 2. DEFINITIONS

- **"API"** — The Regime Classifier API accessible at https://regime-api.onrender.com
- **"x402"** — The HTTP 402 micropayment protocol for API access
- **"USDC"** — USD Coin stablecoin on the Base blockchain (eip155:8453)
- **"Transaction"** — A single API query paid via x402 micropayment
- **"Revenue"** — Gross USD value of all USDC payments received via x402

---

## 3. GRANT OF RIGHTS

### 3.1 Sentinel Grants
Sentinel grants Partner the non-exclusive right to facilitate x402 payments for the API in exchange for the revenue split defined in Section 4.

### 3.2 Partner Grants
Partner grants Sentinel the right to list the partnership in marketing materials, co-author blog posts, and credit Partner's infrastructure in API documentation.

### 3.3 Non-Exclusive
Both parties retain the right to pursue other partnerships. Sentinel may develop x402 integrations with other providers. Partner may facilitate payments for other APIs.

---

## 4. REVENUE SPLIT

### 4.1 Payment Mechanism
All x402 transactions are settled directly to Sentinel's USDC wallet on Base:
```
Wallet Address: 0xF1484AB5d105F238ebdaA88cf861D384EC7f3Eaa
Network: Base (eip155:8453)
```

### 4.2 Revenue Share (Select One)

**OPTION A: 80/20 Revenue Share (Recommended)**
- Sentinel receives 80% of gross transaction revenue
- Partner receives 20% of gross transaction revenue
- Settlement: Monthly, within 5 business days of month-end
- Minimum partner take: $10/month (to cover USDC transfer costs)

Example calculation (1,000 queries × $0.003):
- Gross: $3.00
- Sentinel: $2.40
- Partner: $0.60

**OPTION B: Flat Facilitation Fee**
- Partner charges $0.001 USDC per transaction
- Sentinel retains remainder
- Settlement: Bi-weekly or monthly, as agreed
- Minimum charge: $5/month

Example calculation (1,000 queries × $0.003):
- Gross: $3.00
- Partner Fee: $1.00 (1,000 × $0.001)
- Sentinel: $2.00

**OPTION C: Hybrid Model**
- 0-100 queries/day: 80/20 revenue share
- 100+ queries/day: Flat $0.001/transaction facilitation fee
- Settlement: Monthly, within 5 business days

---

## 5. IMPLEMENTATION & DEPLOYMENT

### 5.1 Timeline
- **Phase 1 (Week 1):** Integration and testing (March 1-7)
- **Phase 2 (Week 2):** Launch and announcement (March 8-14)
- **Phase 3 (Weeks 3-4):** Optimization and growth (March 15-28)

### 5.2 Integration Responsibilities

**Partner Will Provide:**
- x402 payment facilitator endpoint/service
- Documentation on how to integrate with Sentinel's API
- Testnet environment for validation
- Blockchain settlement infrastructure

**Sentinel Will Provide:**
- x402-compatible middleware
- API documentation
- Integration support (24-hour response time)
- Revenue reporting and analytics

### 5.3 Testing & Validation
- 2-week testing period on testnet (no real payments)
- Partner and Sentinel validate payment flow
- Test with minimum 100 transactions
- Confirm USDC settlement to Sentinel's wallet
- Document any integration issues

### 5.4 Production Launch
- Upon successful testnet validation, deploy to mainnet
- Monitor for 48 hours with reduced query limits
- Scale to full production
- Begin marketing campaign

---

## 6. FINANCIAL TERMS

### 6.1 Monthly Reporting
Partner will provide Sentinel with a monthly report by the 3rd of each month containing:
- Total transactions processed
- Total revenue generated
- Partner's share (20% or facilitation fees as applicable)
- Any failed transactions or refunds

### 6.2 Settlement
- Partner settles Sentinel's share within 5 business days of month-end
- Payment method: USDC transfer to Sentinel's Base wallet
- If revenue <$10/month, settlement deferred to following month

### 6.3 Audit Rights
Sentinel may audit Partner's transaction records upon 30 days' notice, not more than once per year. All records will be kept confidential.

### 6.4 No Warranties
Partner makes no guarantee of minimum transaction volume or revenue.

---

## 7. OBLIGATIONS & PERFORMANCE

### 7.1 Sentinel's Obligations
- Maintain 99.5% uptime for API endpoints (measured monthly)
- Respond to integration issues within 24 hours
- Provide monthly usage analytics
- Update API documentation quarterly
- Refresh regime classifier data monthly
- Participate in quarterly partnership review calls

### 7.2 Partner's Obligations
- Maintain x402 payment facilitator with 99% uptime
- Process all valid x402 transactions within 60 seconds
- Settle payments within 5 business days of month-end
- Respond to payment disputes within 24 hours
- Provide usage reports on request
- Support joint marketing and co-announcements

### 7.3 Support SLA
- Critical issues (API down): 1-hour response time
- Payment processing failures: 4-hour response time
- Integration questions: 24-hour response time

---

## 8. INTELLECTUAL PROPERTY

### 8.1 Ownership
- Sentinel retains all IP rights to the Regime API
- Partner retains all IP rights to the x402 infrastructure
- Neither party will copy or reverse-engineer the other's technology

### 8.2 Attribution
- Sentinel will credit Partner in API documentation as "Powered by [Partner Name] x402 Infrastructure"
- Partner will credit Sentinel in marketplace listings as "Regime Classifier by Sentinel Algorithms"

---

## 9. CONFIDENTIALITY

### 9.1 Confidential Information
Both parties agree to keep the following confidential:
- Pricing terms and revenue splits
- Technical integration details
- Monthly revenue reports
- User/transaction data
- Strategic plans discussed in partnership calls

### 9.2 Permitted Disclosures
Each party may disclose confidential information:
- To professional advisors (lawyers, accountants)
- As required by law or court order
- For co-marketing purposes (with prior approval)

### 9.3 Public Announcements
Any public announcement of this partnership requires written approval from both parties.

---

## 10. TERM & TERMINATION

### 10.1 Term
This Agreement is effective as of the Effective Date and continues for **12 months**, unless earlier terminated.

### 10.2 Renewal
This Agreement will automatically renew for successive 12-month periods unless either party provides written notice of non-renewal at least 30 days before expiration.

### 10.3 Termination for Convenience
Either party may terminate this Agreement upon **30 days' written notice**, without cause.

### 10.4 Termination for Cause
Either party may terminate immediately if:
- The other party materially breaches this Agreement and fails to cure within 15 days
- The other party becomes insolvent or bankrupt
- The other party ceases operations for more than 7 consecutive days

### 10.5 Effect of Termination
Upon termination:
- All x402 payments processed prior to termination are final
- Partner settles Sentinel's final payment within 15 days
- Both parties cease using the other's name/branding
- All confidential information remains protected indefinitely

---

## 11. REPRESENTATIONS & WARRANTIES

### 11.1 Sentinel Represents
- It has the right to license the API for x402 micropayments
- The API does not infringe any third-party IP rights
- The API is provided "as-is" with no warranties of fitness for a particular purpose

### 11.2 Partner Represents
- It has the right to provide x402 payment facilitation services
- Its infrastructure complies with all applicable laws
- It has adequate liability insurance

### 11.3 Disclaimer
EXCEPT AS EXPRESSLY STATED HEREIN, EACH PARTY DISCLAIMS ALL OTHER WARRANTIES, EXPRESS OR IMPLIED, INCLUDING WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.

---

## 12. LIABILITY & INDEMNIFICATION

### 12.1 Limitation of Liability
Neither party is liable for:
- Indirect, consequential, or punitive damages
- Loss of revenue or profit
- Data loss or corruption
- Damages exceeding the total revenue received under this Agreement in the prior 12 months

### 12.2 Mutual Indemnification
Each party will indemnify, defend, and hold harmless the other from any third-party claims arising from:
- Its breach of this Agreement
- Its IP infringement
- Its violation of applicable laws

---

## 13. COMPLIANCE & LEGAL

### 13.1 Regulatory Compliance
- Both parties comply with all applicable laws regarding cryptocurrency, stablecoins, and payment services
- Both parties understand that x402 micropayments involve USDC (stablecoin) on the Base blockchain
- Partner represents that it is authorized to facilitate payments in the jurisdictions where its services are offered

### 13.2 No Partnership/Agency
This Agreement does not create a partnership, joint venture, or agency relationship. Neither party is authorized to bind the other.

### 13.3 Governing Law
This Agreement is governed by the laws of [State], without regard to its conflicts of law principles.

### 13.4 Jurisdiction
Both parties consent to the exclusive jurisdiction of the state and federal courts in [County], [State].

---

## 14. DISPUTE RESOLUTION

### 14.1 Negotiation
Any dispute will first be escalated to both parties' executive leadership for negotiation.

### 14.2 Mediation
If negotiation fails, both parties will submit to non-binding mediation in [City], [State].

### 14.3 Arbitration
If mediation fails, disputes will be resolved by binding arbitration under [AAA/JAMS] rules.

---

## 15. GENERAL PROVISIONS

### 15.1 Entire Agreement
This Agreement constitutes the entire agreement between the parties regarding the subject matter and supersedes all prior negotiations and agreements.

### 15.2 Amendments
Any amendments must be in writing and signed by both parties.

### 15.3 Severability
If any provision is found invalid, the remaining provisions remain in effect.

### 15.4 Assignment
Neither party may assign this Agreement without the other's written consent.

### 15.5 Notices
All notices must be in writing and delivered personally, by email, or by certified mail to:

**For Sentinel:**
[Mitch's Address]
Email: [Email]

**For Partner:**
[Partner Contact Name]
Email: [Email]

### 15.6 Waiver
No waiver of any provision is effective unless in writing and signed by the waiving party.

---

## 16. SIGNATURES

**SENTINEL ALGORITHMS LLC**

By: _________________________
Name: Mitchell [Last Name]
Title: Founder/CEO
Date: _______________________

**[PARTNER LEGAL ENTITY NAME]**

By: _________________________
Name: [Partner Contact Name]
Title: [Title]
Date: _______________________

---

## APPENDIX A: x402 PRICING SCHEDULE

The following pricing schedule is in effect as of the Effective Date. Prices may be updated by mutual agreement.

| Endpoint | Price | Description |
|----------|-------|-------------|
| `/v1/regime/current` | $0.001 USDC | Current market regime |
| `/v1/regime/history` | $0.005 USDC | Historical regime data |
| `/v1/regime/transitions` | $0.003 USDC | Regime transition points |
| `/v1/regime/classify` | $0.01 USDC | Custom classification |
| `/v1/regime/batch` | $0.02 USDC | Batch queries (10+) |

**Free Tier:** First 1,000 transactions/month free (promotional, may be adjusted)

---

## APPENDIX B: INTEGRATION SPECIFICATIONS

### x402 Facilitator Endpoint
[Partner to provide]

### Blockchain Settlement
- Network: Base (eip155:8453)
- Token: USDC (0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913)
- Sentinel Wallet: 0xF1484AB5d105F238ebdaA88cf861D384EC7f3Eaa

### Payment Flow
1. Client sends request to Regime API without payment
2. API returns 402 Payment Required with x402 headers
3. Client signs USDC payment via wallet
4. Client resends request with payment signature
5. API validates signature via x402 facilitator
6. Facilitator settles USDC to Sentinel's wallet
7. API returns requested data

---

## APPENDIX C: PRICING STRATEGY (OPTIONAL)

This appendix outlines potential pricing adjustments based on market conditions:

- **Low volume (<100 queries/day):** Maintain $0.001 for /regime/current
- **High volume (>1,000 queries/day):** Consider reducing to $0.0005 for /regime/current
- **Seasonal adjustments:** Increase prices 10% during earnings season (Jan, Apr, Jul, Oct)
- **Promotional pricing:** Offer 50% discount on first 100 queries to new agents

---

**Document Version:** 1.0 (Template)  
**Last Updated:** Feb 28, 2026  
**Status:** Ready for Legal Review  
**Next Step:** Have a lawyer customize based on your jurisdiction and specific terms with Partner
