import json

new_meds = [
    {"nome": "Nitrofurantoína 100mg", "classificacao": "ANTIBIÓTICOS — Nitrofuranos", "posologia": "100mg a cada 6h por 7 dias (ITU baixa)", "indicacao": "", "status": "Disponível"},
    {"nome": "Fluconazol 150mg", "classificacao": "ANTIFÚNGICOS", "posologia": "150mg dose única (candidíase vaginal); 100-400mg/dia (outras)", "indicacao": "", "status": "Disponível"},
    {"nome": "Miconazol creme", "classificacao": "ANTIFÚNGICOS", "posologia": "Aplicar 2x/dia por 2-4 semanas (tinea) ou 7 dias (vaginal)", "indicacao": "", "status": "Disponível"},
    {"nome": "Nistatina suspensão", "classificacao": "ANTIFÚNGICOS", "posologia": "1-2mL (100.000-200.000UI) 4x/dia após refeições (candidíase oral)", "indicacao": "", "status": "Disponível"},
    {"nome": "Nistatina + Óxido de Zinco pomada", "classificacao": "ANTIFÚNGICOS", "posologia": "Aplicar na área afetada (fraldas/candidíase cutânea) 2-4x/dia após higiene", "indicacao": "", "status": "Disponível"},
    {"nome": "Albendazol 400mg cp", "classificacao": "ANTIPARASITÁRIOS / ANTIELMÍNTICOS", "posologia": "400mg dose única (helmintos intestinais)", "indicacao": "", "status": "Disponível"},
    {"nome": "Albendazol gotas 40mg/mL", "classificacao": "ANTIPARASITÁRIOS / ANTIELMÍNTICOS", "posologia": "200mg (5mL) dose única < 2 anos; 400mg >= 2 anos", "indicacao": "", "status": "Disponível"},
    {"nome": "Ivermectina 6mg", "classificacao": "ANTIPARASITÁRIOS / ANTIELMÍNTICOS", "posologia": "0,2mg/kg/dose única (estrongiloidíase, escabiose)", "indicacao": "", "status": "Disponível"},
    {"nome": "Permetrina 5%", "classificacao": "ANTIESCABIÓTICOS / PEDICULICIDAS", "posologia": "Aplicar no corpo (noite), lavar após 8-14h; repetir em 7 dias", "indicacao": "", "status": "Disponível"},
    {"nome": "Acetilcisteína xarope 20mg/mL", "classificacao": "MUCOLÍTICOS / EXPECTORANTES", "posologia": "200mg (10mL) a cada 8h (adultos); 100mg 2-3x/dia (crianças)", "indicacao": "", "status": "Disponível"},
    {"nome": "Cloridrato de Ambroxol 30mg/5mL", "classificacao": "MUCOLÍTICOS / EXPECTORANTES", "posologia": "30mg (5mL) 2-3x/dia (adultos); 15mg 2-3x/dia (crianças 2-6 anos)", "indicacao": "", "status": "Disponível"},
    {"nome": "Cloreto de Sódio 0,9% spray nasal", "classificacao": "DESCONGESTIONANTES / HIGIENE NASAL", "posologia": "1-3 jatos em cada narina, 2-6x/dia (higiene nasal)", "indicacao": "", "status": "Disponível"},
    {"nome": "Norestin cp (Noretisterona 0,35mg)", "classificacao": "ANTICONCEPCIONAIS HORMONAIS", "posologia": "1 cp/dia continuamente, mesma hora (minipílula)", "indicacao": "", "status": "Disponível"},
    {"nome": "Ciclo 21 cp (Etinilestradiol + Levonorgestrel)", "classificacao": "ANTICONCEPCIONAIS HORMONAIS", "posologia": "1 cp/dia por 21 dias -> 7 dias de pausa", "indicacao": "", "status": "Disponível"},
    {"nome": "Depo-Provera inj. (Acetato de Medroxiprogesterona 150mg)", "classificacao": "ANTICONCEPCIONAIS HORMONAIS", "posologia": "150mg IM a cada 3 meses", "indicacao": "", "status": "Disponível"},
    {"nome": "Mesigyna inj. (Noretisterona 50mg + Estradiol 5mg)", "classificacao": "ANTICONCEPCIONAIS HORMONAIS", "posologia": "1 ampola IM/mês (ciclos de 28-30 dias)", "indicacao": "", "status": "Disponível"},
    {"nome": "Cyclofemina inj. (Medroxiprogesterona 25mg + Cipionato de Estradiol 5mg)", "classificacao": "ANTICONCEPCIONAIS HORMONAIS", "posologia": "1 ampola IM/mês", "indicacao": "", "status": "Disponível"},
    {"nome": "Acetato de Medroxiprogesterona 25mg + Cipionato de Estradiol 5mg", "classificacao": "ANTICONCEPCIONAIS HORMONAIS", "posologia": "1 ampola IM/mês", "indicacao": "", "status": "Disponível"},
    {"nome": "Finasterida 5mg", "classificacao": "UROPATIA OBSTRUTIVA / PRÓSTATA — Alfabloqueadores e Inibidores da 5-alfa-redutase", "posologia": "5mg/dia, 1x/dia (HPB); efeito pleno em 6-12 meses", "indicacao": "", "status": "Disponível"},
    {"nome": "Doxazosina Mesilato 4mg", "classificacao": "UROPATIA OBSTRUTIVA / PRÓSTATA — Alfabloqueadores e Inibidores da 5-alfa-redutase", "posologia": "4-8mg/dia, 1x/dia (HPB / HAS), início com dose menor", "indicacao": "", "status": "Disponível"},
    {"nome": "Amitriptilina 25mg", "classificacao": "PSICOFÁRMACOS — Antidepressivos", "posologia": "25-150mg/dia; iniciar com 25mg à noite; ajustar gradualmente", "indicacao": "", "status": "Disponível"},
    {"nome": "Amitriptilina 75mg", "classificacao": "PSICOFÁRMACOS — Antidepressivos", "posologia": "75-150mg/dia à noite; dose de manutenção", "indicacao": "", "status": "Disponível"},
    {"nome": "Clomipramina 10mg", "classificacao": "PSICOFÁRMACOS — Antidepressivos", "posologia": "10-250mg/dia; iniciar com 10-25mg; dose única noturna ou dividida", "indicacao": "", "status": "Disponível"},
    {"nome": "Clomipramina 25mg", "classificacao": "PSICOFÁRMACOS — Antidepressivos", "posologia": "25-250mg/dia; dose habitual 100-150mg/dia", "indicacao": "", "status": "Disponível"},
    {"nome": "Fluoxetina 20mg", "classificacao": "PSICOFÁRMACOS — Antidepressivos", "posologia": "20-60mg/dia, 1x/dia (manhã), início 20mg/dia", "indicacao": "", "status": "Disponível"},
    {"nome": "Nortriptilina 25mg", "classificacao": "PSICOFÁRMACOS — Antidepressivos", "posologia": "25-150mg/dia; iniciar com 25mg; preferir dose noturna", "indicacao": "", "status": "Disponível"},
    {"nome": "Nortriptilina 50mg", "classificacao": "PSICOFÁRMACOS — Antidepressivos", "posologia": "50-150mg/dia; dose de manutenção", "indicacao": "", "status": "Disponível"},
    {"nome": "Clorpromazina 25mg", "classificacao": "PSICOFÁRMACOS — Antipsicóticos", "posologia": "25-300mg/dia em 2-4 doses, iniciar com dose baixa", "indicacao": "", "status": "Disponível"},
    {"nome": "Clorpromazina 100mg", "classificacao": "PSICOFÁRMACOS — Antipsicóticos", "posologia": "100-600mg/dia em doses divididas (esquizofrenia)", "indicacao": "", "status": "Disponível"},
    {"nome": "Haloperidol 1mg", "classificacao": "PSICOFÁRMACOS — Antipsicóticos", "posologia": "1-20mg/dia em 2-3 doses; ajustar conforme resposta", "indicacao": "", "status": "Disponível"},
    {"nome": "Haloperidol 5mg", "classificacao": "PSICOFÁRMACOS — Antipsicóticos", "posologia": "5-20mg/dia em 2-3 doses", "indicacao": "", "status": "Disponível"},
    {"nome": "Decanoato de Haloperidol 50mg/mL", "classificacao": "PSICOFÁRMACOS — Antipsicóticos", "posologia": "50-200mg IM a cada 4 semanas (depósito)", "indicacao": "", "status": "Disponível"},
    {"nome": "Carbonato de Lítio 300mg", "classificacao": "PSICOFÁRMACOS — Estabilizadores do Humor", "posologia": "300-1200mg/dia em 2-3 doses; monitorar litemia (0,6-1,2 mEq/L)", "indicacao": "", "status": "Disponível"},
    {"nome": "Ácido Valproico 250mg", "classificacao": "PSICOFÁRMACOS — Estabilizadores do Humor", "posologia": "250-1500mg/dia em 2-3 doses; ajustar por nível sérico", "indicacao": "", "status": "Disponível"},
    {"nome": "Ácido Valproico 500mg", "classificacao": "PSICOFÁRMACOS — Estabilizadores do Humor", "posologia": "500-1500mg/dia em 2-3 doses", "indicacao": "", "status": "Disponível"},
    {"nome": "Valproato de Sódio 50mg/mL", "classificacao": "PSICOFÁRMACOS — Estabilizadores do Humor", "posologia": "Dose conforme peso e indicação; monitorar nível sérico", "indicacao": "", "status": "Disponível"},
    {"nome": "Carbamazepina 200mg", "classificacao": "PSICOFÁRMACOS — Anticonvulsivantes / Antiepilépticos", "posologia": "200-1200mg/dia em 2-3 doses; iniciar com 100-200mg/dia", "indicacao": "", "status": "Disponível"},
    {"nome": "Carbamazepina 400mg", "classificacao": "PSICOFÁRMACOS — Anticonvulsivantes / Antiepilépticos", "posologia": "400-1200mg/dia em 2-3 doses (dose de manutenção)", "indicacao": "", "status": "Disponível"},
    {"nome": "Carbamazepina 20mg/mL", "classificacao": "PSICOFÁRMACOS — Anticonvulsivantes / Antiepilépticos", "posologia": "Dose conforme peso/idade; crianças: 10-20mg/kg/dia em 2-3 doses", "indicacao": "", "status": "Disponível"},
    {"nome": "Clonazepam 2mg", "classificacao": "PSICOFÁRMACOS — Anticonvulsivantes / Antiepilépticos", "posologia": "0,5-20mg/dia em 2-3 doses; início com 0,5-1mg", "indicacao": "", "status": "Disponível"},
    {"nome": "Clonazepam gotas 2,5mg/mL", "classificacao": "PSICOFÁRMACOS — Anticonvulsivantes / Antiepilépticos", "posologia": "0,1mg/kg/dia dividido (crianças); adultos iniciar 0,5-1mg/dia", "indicacao": "", "status": "Disponível"},
    {"nome": "Fenobarbital 100mg", "classificacao": "PSICOFÁRMACOS — Anticonvulsivantes / Antiepilépticos", "posologia": "1-3mg/kg/dia em 1-2 doses; adultos 60-180mg/dia", "indicacao": "", "status": "Disponível"},
    {"nome": "Fenobarbital 40mg/mL", "classificacao": "PSICOFÁRMACOS — Anticonvulsivantes / Antiepilépticos", "posologia": "Dose conforme peso; crianças: 3-5mg/kg/dia", "indicacao": "", "status": "Disponível"},
    {"nome": "Fenitoína 100mg", "classificacao": "PSICOFÁRMACOS — Anticonvulsivantes / Antiepilépticos", "posologia": "4-7mg/kg/dia em 1-3 doses; monitorar nível sérico (10-20mcg/mL)", "indicacao": "", "status": "Disponível"},
    {"nome": "Diazepam 10mg", "classificacao": "PSICOFÁRMACOS — Ansiolíticos / Benzodiazepínicos", "posologia": "2-10mg a cada 6-12h (ansiedade/espasmo muscular), uso curto prazo", "indicacao": "", "status": "Disponível"},
    {"nome": "Biperideno 2mg", "classificacao": "PSICOFÁRMACOS — Antiparkinsonianos (uso em psiquiatria)", "posologia": "2-8mg/dia em 3-4 doses (controle de efeitos extrapiramidais)", "indicacao": "", "status": "Disponível"}
]

with open('data/medicamentos.json', 'r', encoding='utf-8') as f:
    existing_meds = json.load(f)

existing_names = {m['nome'] for m in existing_meds}
added = 0

for m in new_meds:
    if m['nome'] not in existing_names:
        existing_meds.append(m)
        added += 1

if added > 0:
    with open('data/medicamentos.json', 'w', encoding='utf-8') as f:
        json.dump(existing_meds, f, indent=2, ensure_ascii=False)
    print(f"Adicionados {added} novos medicamentos ao JSON.")
else:
    print("Nenhum medicamento novo para adicionar.")
