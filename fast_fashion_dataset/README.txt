# Fast Fashion Network

**Flora & Radiah · Complex Networks · White paper**

The fast fashion industry depends on cheap labour, cheap materials and unsafe working conditions, and its production is concentrated in a few Asian countries. We model global clothing trade as a network of countries, combined with a simple supply-and-demand market. This lets us see what happens to production, prices and wages when a hub is hit, when ethical and environmental rules get stricter, and when industry grows.

---

## 1. Research questions

1. **Hub shocks:** what happens to the global textile supply chain when a hub is hit (strikes, collapses, fires)?
2. **Rules:** how do ethical and environmental rules change the network?
3. **Wages:** do more factories in a country push wages up, and does production then move?

---

## 2. The network

A directed, weighted, bipartite network of countries.

| Node type | Countries | Attributes |
|---|---|---|
| Producer *i* | China, Bangladesh, Vietnam, India, Turkey, Indonesia, Pakistan, Cambodia | factories F_i, average monthly wage W_i (USD), worker safety score S_i (0–10), environmental regulation score E_i (0–10), capacity K_i, unit cost c_i, production P_i |
| Consumer *j* | EU, USA, Japan, UK, South Korea | demand curve D_j(p), consumption C_j |
| Brand (Sim 2 only) | Brand A, Brand B | ethical threshold T |
| Factory (Sim 1.5 and 3 only) | peripheral nodes attached to their country | — |

**Edges:** producer → consumer, weighted by the volume of clothing exported, w_ij.

---

## 3. The economic model (macro perspective)

**Supply.** Each producer produces more when the price is higher, up to its capacity:

S_i(p) = min( K_i , s_i · (p − c_i) ) for p > c_i, otherwise 0

- c_i is the unit cost: mostly labour, c_i = λ · W_i, raised by environmental rules (Sim 4).
- s_i is how strongly production reacts to price.

**Demand.** Each consumer market buys less when the price is higher:

D_j(p) = A_j − B_j · p

**Equilibrium.** There are no shipping costs, so there is one world price p*. It's the price where total supply meets total demand:

Σ_i S_i(p*) = Σ_j D_j(p*) = Q*

Then P_i = S_i(p*) and C_j = D_j(p*).

**Edges.** The balance equations do not fix who sells to whom. With 8 producers and 5 consumers there are (8−1)(5−1) = 28 free values. We use the standard maximum-entropy assumption, proportional allocation, where every producer splits its output in the same proportions as the consumers' demand:

w_ij = P_i · C_j / Q*

**How a shock works.** Every event in our simulations shifts a supply curve:
- **Collapse or strike:** capacity K_i drops, so the curve shifts left.
- **Wage rise or stricter rules:** cost c_i goes up, so the curve shifts up.

We then solve for the new equilibrium. The price rises, total quantity falls, the other producers move up their supply curves and take over part of the production, and consumers buy a bit less. So production is redistributed by price, not by a hand-made rule.

---

## 4. Measures and outcomes

**Network measures**
- **Weighted degree (strength):** total production of each country. Is production concentrated in a few hubs?
- **Eigenvector centrality:** which producer matters most. The network only has producer → consumer edges and no loops, so we compute it on the undirected weighted network (Week 4).
- **Null model:** the proportional flows P_i · C_j / Q*. Real BACI links stronger than this are stronger than country size alone explains (same idea as k_i k_j / 2m in modularity, Week 5).

**Outcomes**

| Outcome | Formula | Used in |
|---|---|---|
| World price | p* | all |
| Total quantity traded | Q* (after) / Q* (before) | Sim 1, 1.5 |
| Concentration | share of the biggest producer in Q* | Sim 1, 2, 3 |
| Average wage per unit | W̄ = Σ P_i W_i / Σ P_i | Sim 2, 3 |
| Environmental impact | Σ P_i (10 − E_i) | Sim 2, 4 |

---

## 5. Simulations

**Sim 1: Removing the biggest hub (failure vs. attack, percolation, Week 4)**
- **Targeted attack:** remove a fraction f of the factories of the producer with the highest eigenvector centrality, from 0 to 1 in steps of 0.05. Removing a share f of factories removes that share of its current output, so its capacity becomes K_i = (1 − f) · P_i. Then we solve for the new equilibrium.
- **Random failure (control):** cut the same amount of capacity from random producers.
- **Plot:** Q* and p* vs. fraction removed, plus which countries take over the production.
- **Prediction:** a random failure barely moves the price, but attacking the biggest hub raises p* sharply and Q* drops, because the other producers hit their capacity limits.

**Sim 1.5: Rana Plaza (2013)**
- Add a few factory nodes to Bangladesh and stop the Rana Plaza factories completely. This shifts Bangladesh's supply curve slightly left.
- Compare with what really happened: exports kept growing, and Koenig & Poncet (2019) measured how imports from Bangladesh changed for countries whose brands were linked to Rana Plaza.
- **Prediction:** a small left shift barely changes Bangladesh's exports or the world price.

**Sim 2: Brand ethics (Schelling-type threshold model, Week 6)**
- **Brand A (zero ethics, based on Shein):** buys from all producers, so it pays the normal world price p*.
- **Brand B (ethical, based on H&M):** only buys from producers with safety score S_i ≥ T. Its market only includes the supply curves of those countries, so it has its own equilibrium price p*_B. If a country falls below T, Brand B is "dissatisfied" and moves its orders, like agents in the Schelling model.
- **Experiment:** sweep T and each brand's share of total demand.
- **Measure:** the **ethics premium** p*_B − p*_A, plus where each brand sources from, the average wage, environmental impact and concentration of each brand's supply chain.
- **Prediction:** the higher T, the fewer countries Brand B can use, so its price rises and its production concentrates in one or two countries. That makes it more exposed when one of them is hit.

**Sim 3: Industry growth and wages (preferential attachment, Barabási–Albert)**
- New factories join producer *i* with probability proportional to F_i · (W_ref / W_i): many existing factories and a low average wage make a country attractive. Each new factory adds capacity K_i.
- Wages follow the demand for workers: dW_i/dt = a · F_i − b · (W_i − W0_i). Higher wages raise c_i, which shifts the country's supply curve up. Wages are compared in PPP.
- **Experiment A (baseline):** grow the network and compare the final factory distribution with real factory counts.
- **Experiment B (wage shock):** raise Bangladesh's wage from the current Tk 12,500 minimum toward the workers' demand of Tk 30,000 (+140%), sweeping 0–140%. Solve for the new equilibrium each time.
- **Hypothesis:** more industry pushes wages up, which raises costs, so production and new factories move to the next cheapest country.

**Sim 4: Pollution haven effect**
- Stricter environmental rules raise the unit cost: c_i = λ · W_i · (1 + κ · E_i / 10).
- Pollution builds up with first-order kinetics (reaction kinetics lecture): dQ_i/dt = (10 − E_i) · P_i − δ · Q_i.
- **Experiment:** raise E_i in one hub, so its supply curve shifts up, and solve for the new equilibrium.
- **Prediction:** the hub produces less, cheaper countries with weaker rules produce more, and total pollution barely drops.

---

## 6. Parameters

These are the parameters from Outline (Draft 2), which we use to simulate the real events, plus the new parameters the economic model needs. Every value is from data unless it says "chosen."

### Network

1. **Producer countries:** China, Bangladesh, Vietnam, India, Turkey, Indonesia, Pakistan, Cambodia
   - Reason: the biggest clothing exporters. China has 29.64% of the world market and Bangladesh 6.90% (WTO 2024).
   - Source: [The Daily Star](https://www.thedailystar.net/business/news/bangladesh-retains-2nd-spot-global-apparel-exports-3935421)
2. **Consumer countries:** EU, US, Japan, UK, South Korea
   - Reason: together about 62% of world clothing imports: EU 35.8%, US 15.7%, Japan 4.5%, UK 3.8%, South Korea 2.3% (WTO 2023).
   - Source: [Fibre2Fashion](https://fibre2fashion.com/news/apparel-news/china-2023-s-top-global-rmg-exporter-bangladesh-2nd-vietnam-3rd-wto-297174-newsdetails.htm)
3. **Edge weights w_ij:** export value from producer i to consumer j
   - Value: from data (HS 61 + HS 62, 2024). Real flows are compared with the proportional flows P_i·C_j / Q*.
   - Check: row sums should match the WTO totals: China $165.24bn, Bangladesh $38.48bn, Vietnam $33.94bn, Turkey $17.91bn, India $16.36bn, Cambodia $9.89bn, Pakistan $9.28bn, Indonesia $8.73bn.
   - Until BACI is downloaded, the dataset uses estimated weights from proportional allocation (edges_estimated.csv).
   - Source: BACI, CEPII (link in catalog). WTO totals: [Fibre2Fashion](https://www.fibre2fashion.com/news/apparel-news/china-top-apparel-exporter-in-2024-bangladesh-2nd-303822-newsdetails.htm)
4. **Factories per country F_i:**
   - Bangladesh 3,320 (Mapped in Bangladesh, current count; link in catalog).
   - China 13,745 (garment enterprises above designated size, 2025). Source: [texleader](https://texleader.com.cn/en/news-35400.html)
   - Vietnam 13,741 (textile and garment enterprises, 2019) and Cambodia 800 (June 2022). Source: [ASEAN report](https://asean.org/wp-content/uploads/2024/12/Textiles-Industry-in-CLMV-Economies.pdf)
   - Other countries from [Open Supply Hub](https://info.opensupplyhub.org/premium-data-downloads-analysis).
   - ⚠️ Definitions differ by country.
5. **Starting wage W0_i (USD per month):**
   - Bangladesh 102, India 124, Pakistan 135, Vietnam 163, Indonesia 172, Cambodia 208 (garment minimum wage, H&M Group data). Source: [Prothom Alo](https://en.prothomalo.com/business/local/jjf2ngpr30)
   - China 482 (ILO). Source: [The Daily Star](https://www.thedailystar.net/news/bangladesh/news/the-low-value-trap-4317331)
   - Turkey 655 (national net minimum wage 2026, TRY 28,075). Source: [Hürriyet Daily News](https://hurriyetdailynews.com/turkiye-increases-minimum-wage-by-27-percent-for-2026-217121)
   - Average wages in PPP: ILOSTAT (link in catalog).
6. **Rights rating r_i (ITUC 2026, 1 = best, 5 = worst) → safety score S_i = 2·(6 − r_i):**
   - 5 for Bangladesh, China, India, Pakistan, Cambodia, Indonesia and Turkey (S = 2). 4 for Vietnam (S = 4).
   - Lowered for countries with many incidents ([textile-incidents.info](https://textile-incidents.info/cases/list-of-cases.html)).
   - Sources: [Financial Express](https://thefinancialexpress.com.bd/trade/workers-rights-ranking-bangladesh-moves-out-of-worlds-top-10-worst-nations), [ITUC 2026 PDF](https://news.industriall-europe.eu/documents/upload/2026/6/639159852713552724_ITUC_global_rights_index_2026.pdf)

### Economic model (new)

7. **Baseline price p0 = 1 (normalized), demand elasticity ε = 0.5 (swept)**
   - Demand: B_j = ε · C_j / p0 and A_j = C_j + B_j · p0, so each market buys exactly its 2024 imports at p0.
8. **Unit cost c_i = λ · W_i / W_max, λ = 0.5 (swept)**
   - Reason: labour is the main cost of garment production. Dividing by the highest wage keeps every cost below p0.
   - Supply slope: s_i = P_i / (p0 − c_i), so each country produces exactly its 2024 exports at p0.
9. **Capacity K_i = P_i · (1 + spare share), spare share = 0.2 (swept)**
   - Reason: no data on spare capacity, so we choose a value and sweep it.
10. **Closed system:** the 5 markets import more than the 8 producers export (they also buy from the EU and others), so demand is scaled to the 5 markets' shares of total production: Σ C_j = Σ P_i = $299.8bn. Price per producer for checking: export value / tonnes from BACI.

### Simulation 1: removing a hub

11. **Attack fraction f = 0.16, applied as K_i = (1 − f) · P_i**
    - Reason: 529 factories disrupted on 1 November 2026 (BGMEA), out of 3,320 factories in Bangladesh.
    - Source: BGMEA situation reports (link in catalog). Background: [US News / Reuters](https://www.usnews.com/news/top-news/articles/2026-10-31/bangladesh-to-form-wage-board-after-garment-protests-shut-factories)
12. **Range of fractions tested: 0 to 1 in steps of 0.05**
    - Reason: gives the percolation-style curve of Q* and p* vs. fraction removed (Week 4 slides).
13. **Random failure (control):** the same fraction f, removed from random countries
    - Reason: failure vs. attack comparison (Week 4 slides).
14. **Exit rate after a scandal x = 0.05 per month (low)**
    - Reason: after Rana Plaza, Bangladesh's exports still rose about 16% to $23.86bn, and brands pushed prices down about 6% instead of leaving. Source: [The Daily Star](https://www.thedailystar.net/garment-exports-show-resilience-21162)
    - The stock market barely punished retailers: Jacobs & Singhal (2017), *Journal of Operations Management* (link in catalog).
15. **Redistribution:** decided by the new market equilibrium (section 3). This replaces the draft's proportional-to-volume rule.

### Simulation 2: exploiting vs. non-exploiting brand

16. **Brand A threshold T_A = none**
    - Reason: based on Shein, which got an F in the 2025 Fossil-Free Fashion Scorecard.
    - Source: [EHN](https://www.ehn.org/hm-tops-fashion-climate-rankings-while-shein-and-zara-trail-behind)
17. **Brand B threshold T_B on the safety score, swept from 0 to 10**
    - Reason: based on H&M, which got a B+ (same source). T_B = 4 corresponds to the draft's "ITUC rating ≤ 4".
18. **Compliance weight w_c = 0.04**
    - Reason: compliant factories got about 4% more orders.
    - Source: Distelhorst & Locke (2018), *American Journal of Political Science* 62(3) (link in catalog).
19. **Switching cost s = 0.1 (swept):** at most 10% of an edge's weight can move per month
    - Reason: buyer–supplier relationships are sticky. The exact value is our choice.
    - Source: Amengual & Distelhorst (2019), MIT working paper (link in catalog).
20. **Brand A's share of total demand = 0.5, swept from 0 to 1**
    - Reason: experiment variable.

### Simulation 3: industry growth and wages

21. **Time step = 1 month, run 1995–2025 (360 steps)**
    - Reason: BACI data starts in 1995 (link in catalog).
22. **New factories per step ΔF = 8 per month**
    - Reason: 128 new factories joined BGMEA in 15 months, roughly 100 per year.
    - Source: [Prothom Alo](https://en.prothomalo.com/business/local/28c1y6vs76)
23. **Attachment probability ∝ F_i · (W_ref / W_i)**
    - Reason: preferential attachment (Barabási–Albert) times how cheap the country is (average wage).
24. **Wage growth from factory demand, a: fitted**
    - Reason: fitted to the Bangladesh wage history: Tk 627 (1985), 940 (1994), 1,662.50 (2006), 3,000 (2010), 5,300 (2013), 8,000 (2018), 12,500 (2023).
    - Sources: [TBS](https://www.tbsnews.net/node/763802), [Prothom Alo](https://en.prothomalo.com/business/local/jjf2ngpr30)
25. **Wage pull back toward W0, b: fitted**
    - Reason: fitted to the same series.
    - Validation: since 1994, wages rose eightfold in taka and threefold in USD, while export earnings rose 23 times in USD. Source: [The Daily Star](https://www.thedailystar.net/opinion/views/news/minimum-wage-offer-tk-12500-even-logical-3476266)
26. **Wage review interval = 60 steps**
    - Reason: Bangladesh reviews the garment minimum wage once every five years.
    - Source: [Cornell GLI brief](https://ilr.cornell.edu/sites/default/files-d8/2024-11/cornell-gli-brief-bangladesh-november-2024.pdf)
27. **Wage shock (Experiment B): +0% to +140%**
    - Reason: current minimum Tk 12,500 vs. the workers' demand of Tk 30,000 (2026 strike).

### Simulation 4: environment

28. **Environmental regulation score E_i (0–10) = EPI score / 10**
    - Values: China 3.39, Turkey 3.43, Cambodia 3.12, Pakistan 2.90, Indonesia 2.62, Vietnam 2.38, Bangladesh 2.35, India 2.25.
    - Reason: replaces the draft's per-unit impact (Flora's comment).
    - Source: Environmental Performance Index 2026, Yale/Columbia: [Southern Asia](https://epi.yale.edu/node/51149), [Asia-Pacific](https://epi.yale.edu/node/51145), [Eastern Europe](https://epi.yale.edu/node/51146)
29. **Regulation cost factor κ = 0.5 (chosen and swept)**
    - Reason: how much stricter rules add to unit cost. No data.
30. **Carbon intensity of electricity e_i (gCO₂e/kWh):** extra impact measure
    - Temporary values: China 467.1, Bangladesh 590.8, Vietnam 450.8, India 584.0, Cambodia 471.8, Pakistan 345.7, Indonesia 624.5, Turkey 329.7. Source: [lowcarbonpower.org](https://lowcarbonpower.org/ranking?metric=ci)
    - Final values: lifecycle values from Ember via [OWID](https://ourworldindata.org/grapher/carbon-intensity-electricity).
31. **Shipping emission factor = 0.0769 kgCO₂e per TEU-km:** for edge impact, if shipping is added
    - Source: GLEC Framework v3.0 via [Climatiq](https://www.climatiq.io/data/emission-factor/0a684de8-2224-479d-a423-6f31370f81a8)
32. **Environmental recovery rate δ = 0.1 per step (swept)**
    - Reason: no data, so we choose a value and sweep it.
33. **Pollution tipping threshold P_c (swept, optional)**
    - Reason: no data, so we choose a value and sweep it.
34. **Waste share of used-clothing exports = 0.4, swept from 0.2 to 0.6 (optional)**
    - Reason: no official number. Data for the flows: BACI HS 6309 (link in catalog).

### All simulations

35. **Seeds = 10 runs per experiment**
    - Reason: random failure and factory placement are random, so we average over runs.

---

## 7. Evaluation

We set the parameters from real data and check whether the model reproduces real events:
- **Rana Plaza (2013):** Bangladesh's exports still rose about 16% the following year, and brands pushed prices down about 6% ([Daily Star](https://www.thedailystar.net/garment-exports-show-resilience-21162)). Does Sim 1.5 give the same?
- **2026 Bangladesh strike:** which countries gain production in Sim 1 with f = 0.16, and how much does the price move?

Where the model does not match reality, we explain why.

---

## 8. Dataset (folder `fast_fashion_dataset/`)

| File | Contents |
|---|---|
| `producers.csv` | 8 producers: 2024 exports and world share, factories, garment workers, monthly wage (USD), ITUC rating and safety score, EPI and regulation score E, carbon intensity, capacity |
| `consumers.csv` | 5 markets: 2023 imports and world share, share of the 5, demand scaled to total production |
| `edges_estimated.csv` | 40 producer → consumer weights from proportional allocation (to be replaced with BACI) |
| `calibration_assumed.csv` | unit cost c_i, supply slope s_i, capacity K_i, demand A_j and B_j, so the market clears at p0 = 1 with the 2024 values |
| `events.csv` | real events with date, type, deaths, factories affected, attack fraction and outcome (Rana Plaza, Tazreen, Ali Enterprises, 2023 and 2026 strikes, 2005 quota end) |
| `bangladesh_wage_history.csv` | minimum wage 1985–2026 and export points, for fitting a and b |
| `export_share_history.csv` | world clothing export shares of China, Bangladesh and Vietnam over time |
| `brands.csv` | Shein (Brand A), H&M (Brand B), Zara: grades and thresholds |
| `parameters.csv` | all 35 parameters with value, unit, status (data / chosen / fitted) and source |

**Check:** with this calibration the market clears at p* = 1.00 and Q* = $299.8bn. A 16% attack on Bangladesh gives p* = 1.011 and Q* = $298.1bn; a 16% attack on China gives p* = 1.084 and Q* = $287.3bn.

---

## 9. Open questions

- **Price data:** we have export values (USD), not prices and quantities separately. BACI also gives tonnes, so value / tonnes can serve as a rough price per producer.
- **Elasticities:** ε, λ and the spare share have no direct data. They are set so the baseline matches 2024 and then swept.
- **Null model:** is proportional allocation enough, or should we also use Erdős–Rényi? (Ask the professor.)
- **Missing data:** factory counts for Turkey, India, Pakistan and Indonesia (Open Supply Hub), average wages in PPP, a source for the 2026 Foshan fire.
- **Proof of concept:** a toy model (countries as letters) is built; next step is to run the supply-and-demand model on this dataset.
