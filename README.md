





# Ansätze

## Physical Modelling

### Ziele:
- Gewünschte Resonanz mit statischer Simulation und Dirac-Anregung erzeugen
  - Niedrigere Dämpfung (vielleicht abhängig von der Masse?)
  - Größere Massenunterschiede
  - (Anregung unabhängig von Masse?)
- Wenn das klappt: dynamische Simulation
- Wenn das klappt: andere Anregungen? (Rauschen, Regen)

### Ergebnisse:

#### Transversal:
- 1d transversale Schwinung, hohe Dämpfung, realistische Massen, 44100Hz

[combination_2024_04_09-15_33_17.mp4](results%2Fcombination_2024_04_09-15_33_17.mp4)
- Starke Federn
- Lautstärke passt zur Bewegung
- Keine Informationen über die Form und verschiedene "Körper" (zu rauschig)
- Artefakte?
- Zu tief

[combination_2024_04_09-15_36_53.mp4](results%2Fcombination_2024_04_09-15_36_53.mp4)
- Federn am Limit vor Instabilität
- Etwas höher, aber immer noch zu tief  
- Artefakte immer noch da

---

#### Erste Longitudinal
- 2d Longitudinalschwingung, hohe Dämpfung, starke Federn, realistische Massen, 44100Hz, Abtastung: Durchschnitt orthogonal zur Anregung

[combination_2024_04_10-16_02_02.mp4](results%2Fcombination_2024_04_10-16_02_02.mp4)
- Lautstärke passt okay zur Bewegung
- Änderungen der Federlänge durch Phasen erzeugen störendes Rauschen, unabhängig von Bewegung 
- Keine Informationen über die Form und verschiedene "Körper" (zu rauschig)
- Artefakte

---

#### Longitudinal mit Stride
- 2d Longitudinalschwingung, hohe Dämpfung, starke Federn, realistische Massen, 96kHz, Stride 4,

[combination_2024_04_15-13_51_23_norm_n32_96k_e-15.mp4](results%2Fcombination_2024_04_15-13_51_23_norm_n32_96k_e-15.mp4)
- Abtastung: Durchschnittliche Auslenkung
- Höhere Samplerate verkürzt "Klickschutz" an den Rändern (gefixt)
- Nicht hörbare Bassfrequenzen nehmen Headroom der Audiodatei ein
- Starkes Artefakt besonders am Anfang durch starke Energieänderungen (vor allem durch Federlängen?)
- Wieder kaum Resonanz

[combination_2024_04_15-13_56_29_orth_n32_96k_e-15.mp4](results%2Fcombination_2024_04_15-13_56_29_orth_n32_96k_e-15.mp4)
- Abtastung: Durchschnitt orthogonal zur Anregung
- Artefakte zu Federauslenkung dominieren

[combination_2024_04_15-14_01_05_para_n32_96k_e-15.mp4](results%2Fcombination_2024_04_15-14_01_05_para_n32_96k_e-15.mp4)
- Abstastung: Durchschnitt parallel zur Anregung
- Rauschen durch Federauslenkung nicht mehr so stark
- Artefakt am Start immer noch hörbar