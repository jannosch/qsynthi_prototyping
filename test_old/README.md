





# Ansätze

## Audification



### Ziele



### Ergebnisse

#### Circle of interest

[combination_2024_04_17-14_02_09.mp4](results%2Fmapping%2Fcombination_2024_04_17-14_02_09.mp4)
- Interpolation von Komplexen Zahlen
- initial

[combination_2024_04_17-15_12_28.mp4](results%2Fmapping%2Fcombination_2024_04_17-15_12_28.mp4)
- Interpolation von abs^2
- Kein großer Unterschied zwischen Interpolation vor oder nach abs^2

---

#### Line of interest

[combination_2024_04_18-14_47_45.mp4](results%2Fmapping%2Fcombination_2024_04_18-14_47_45.mp4)
- Interpolation von abs^2
- Grundsätzliche Funktionsfähigkeit von Interpolation bestätigt
- Sauberer Klang
- Starke Ähnlichkeit zum 1D Wavetable mit Tunneleffekt (QSynthi)


## Spektrum-Mapping

### Ziele



### Ergebnisse

#### Manuelles Mapping - Kreis

Parameter:
- Verteilung von 100 bis 4000 Hz
- Simulation:
  - n = 128
  - sim_speed = 0.004
  - sim_fps = 400
- Radius des (Halb)kreises, wenn nicht anders angegeben: 0.6

[combination_2024_04_24-09_47_11.mp4](results%2Fmapping%2Fcombination_2024_04_24-09_47_11.mp4)
- 50 linear verteilte Frequenzen

[combination_2024_04_24-09_54_44.mp4](results%2Fmapping%2Fcombination_2024_04_24-09_54_44.mp4)
- 300 linear verteilte Frequenzen
- Frequenzen löschen sich gegenseitig aus (?)

[combination_2024_04_24-10_00_00.mp4](results%2Fmapping%2Fcombination_2024_04_24-10_00_00.mp4)
- 50 exponentiell verteilte Frequenzen
- Keine regelmäßige Auslöschung mehr
- Natürlicheres Hören (?)

[combination_2024_04_24-09_57_24.mp4](results%2Fmapping%2Fcombination_2024_04_24-09_57_24.mp4)
- 300 exponentiell verteilte Frequenzen
- s.o.
- Bessere Qualität (?)

---

#### Manuelles Mapping - Halbkreis
- Stereo Audio
  - linke Hälfte der Simulation -> linkes Ohr (und umgekehrt)

[combination_2024_04_24-10_04_45.mp4](results%2Fmapping%2Fcombination_2024_04_24-10_04_45.mp4)
- 50 linear verteilte Frequenzen

[combination_2024_04_24-10_06_11.mp4](results%2Fmapping%2Fcombination_2024_04_24-10_06_11.mp4)
- 300 linear verteilte Frequenzen

[combination_2024_04_24-10_06_51.mp4](results%2Fmapping%2Fcombination_2024_04_24-10_06_51.mp4)
- 50 exponentiell verteilte Frequenzen

[combination_2024_04_23-17_19_14.mp4](results%2Fmapping%2Fcombination_2024_04_23-17_19_14.mp4)
- 300 exponentiell verteilte Frequenzen
- Gute räumliche Ortung der Verteilung
- Viele Mitten -> Konzentration der Verteilung um y=0
  - nur mit Vergleichen herauszufinden (siehe Bsp. unten)

[combination_2024_04_24-10_37_27.mp4](results%2Fmapping%2Fcombination_2024_04_24-10_37_27.mp4)
- 300 exponentiell verteilte Frequenzen
- Radius = 0.25
- Unterschied zu vorherigen: größeres Spektrum hörbar, 
schärfere "Wellen" erkennbar -> Wellenberge und -täler (?!)

---

#### Manuelles Mapping - Linie
[combination_2024_04_24-12_00_09.mp4](results%2Fmapping%2Fcombination_2024_04_24-12_00_09.mp4)
- 40 lineare Frequenzen (0-4000 Hz)
- Randomisierte Phasen der Sinusoids




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
- 1d transversale Schwingung, hohe Dämpfung, realistische Massen, 44100Hz

[combination_2024_04_09-15_33_17.mp4](results%2Fphysical_modelling%2Fcombination_2024_04_09-15_33_17.mp4)
- Starke Federn
- Lautstärke passt zur Bewegung
- Keine Informationen über die Form und verschiedene "Körper" (zu rauschig)
- Artefakte?
- Zu tief

[combination_2024_04_09-15_36_53.mp4](results%2Fphysical_modelling%2Fcombination_2024_04_09-15_36_53.mp4)
- Federn am Limit vor Instabilität
- Etwas höher, aber immer noch zu tief  
- Artefakte immer noch da

---

#### Erste Longitudinal
- 2d Longitudinalschwingung, hohe Dämpfung, starke Federn, realistische Massen, 44100Hz, Abtastung: Durchschnitt orthogonal zur Anregung

[combination_2024_04_10-16_02_02.mp4](results%2Fphysical_modelling%2Fcombination_2024_04_10-16_02_02.mp4)
- Lautstärke passt okay zur Bewegung
- Änderungen der Federlänge durch Phasen erzeugen störendes Rauschen, unabhängig von Bewegung 
- Keine Informationen über die Form und verschiedene "Körper" (zu rauschig)
- Artefakte

---

#### Longitudinal mit Stride
- 2d Longitudinalschwingung, hohe Dämpfung, starke Federn, realistische Massen, 96kHz, Stride 4,

[combination_2024_04_15-13_51_23_norm_n32_96k_e-15.mp4](results%2Fphysical_modelling%2Fcombination_2024_04_15-13_51_23_norm_n32_96k_e-15.mp4)
- Abtastung: Durchschnittliche Auslenkung
- Höhere Samplerate verkürzt "Klickschutz" an den Rändern (gefixt)
- Nicht hörbare Bassfrequenzen nehmen Headroom der Audiodatei ein
- Starkes Artefakt besonders am Anfang durch starke Energieänderungen (vor allem durch Federlängen?)
  - Startet zwar in lokalen Energieminimum (alle Phasen sind gleich -> Alle Federn spannen sehr) aber wird sehr schnell instabil bei Phasenänderung der Simulation
- Wieder kaum Resonanz

[combination_2024_04_18-16_35_19_norm_n32_96k_e-15.mp4](results%2Fphysical_modelling%2Fcombination_2024_04_18-16_35_19_norm_n32_96k_e-15.mp4)
- ohne variable Federlängen
- kräftigeres Rauschen im Vergleich zu obigem

[combination_2024_04_15-13_56_29_orth_n32_96k_e-15.mp4](results%2Fphysical_modelling%2Fcombination_2024_04_15-13_56_29_orth_n32_96k_e-15.mp4)
- Abtastung: Durchschnitt orthogonal zur Anregung
- Artefakte zu Federauslenkung dominieren

[combination_2024_04_15-14_01_05_para_n32_96k_e-15.mp4](results%2Fphysical_modelling%2Fcombination_2024_04_15-14_01_05_para_n32_96k_e-15.mp4)
- Abstastung: Durchschnitt parallel zur Anregung
- Rauschen durch Federauslenkung nicht mehr so stark
- Artefakt am Start immer noch hörbar

---

#### Statische Simulation mit Dirac-Anregung
[physical_modelling_2_transverse.ipynb](physical_modelling_2_transverse.ipynb)
````
sample_rate = 4 * 44100

listening = average_listening
excitement_point = np.array([64, 28])

dampening_per_second = 1 - 1e-3
spring_strength = sample_rate * 600
min_mass = 0.01
max_mass = 1

spatial_step = 4

sonification_duration = 3
````

[sonification_2024_04_17-10_42_05_baseline.wav](results%2Fphysical_modelling%2Fsonification_2024_04_17-10_42_05_baseline.wav)
- Massenverteilung: 1
- "Baseline"

[sonification_2024_04_17-10_43_57_static0.wav](results%2Fphysical_modelling%2Fsonification_2024_04_17-10_43_57_static0.wav)
- Massenverteilung: Glockenkurve von frame[0]
- Anregung auf Glockenkurve

[sonification_2024_04_19-09_55_02.wav](results%2Fphysical_modelling%2Fsonification_2024_04_19-09_55_02.wav)
- Massenverteilung: Glockenkurve von frame[0]
- Anregung auf anderen Seite von Glockenkurve
- Gleiche Frequenz nur heller

[sonification_2024_04_17-11_01_45_static0_scaled.wav](results%2Fphysical_modelling%2Fsonification_2024_04_17-11_01_45_static0_scaled.wav)
- Massenverteilung: Glockenkurve von frame[0]
- Abtastung: Gewichteter Durchschnitt von Simulation (Glockenkurve)
- Anregung auf Glockenkurve

[sonification_2024_04_19-10_01_20.wav](results%2Fphysical_modelling%2Fsonification_2024_04_19-10_01_20.wav)
- Massenverteilung: Glockenkurve von frame[0]
- Abtastung: Gewichteter Durchschnitt von Simulation (Glockenkurve)
- Anregung auf anderen Seite von Glockenkurve
- Gleiche Frequenz nur heller


---

#### Statische Simulation mit Dirac-Anregung und invertierten Massen
[physical_modelling_2_transverse.ipynb](physical_modelling_2_transverse.ipynb)
- Massenverteilung: Glockenkurve von frame[0] (siehe min_mass, max_mass)
- Abtastung: Durchschnitt
````
sample_rate = 4 * 44100

listening = average_listening
excitement_point = np.array([64, 28])

dampening_per_second = 1 - 1e-3
spring_strength = sample_rate * 600
min_mass = 1
max_mass = 0.01

spatial_step = 4
````

[sonification_2024_04_22-12_11_31.wav](results%2Fphysical_modelling%2Fsonification_2024_04_22-12_11_31.wav)
- Anregung auf Platte (im Nichts)

[sonification_2024_04_22-15_09_25.wav](results%2Fphysical_modelling%2Fsonification_2024_04_22-15_09_25.wav)
- Anregung auf Schräge der Glockenkurve

[sonification_2024_04_22-12_09_06.wav](results%2Fphysical_modelling%2Fsonification_2024_04_22-12_09_06.wav)
- Anregung direkt auf der Glockenkurve

---

#### Laufende Simulation mit Dirac-Anregung und invertierten Massen
- Massenverteilung: Laufende Simulation (siehe min_mass, max_mass)
- Abtastung: Durchschnitt
- Anregung direkt auf der Glockenkurve
````
sample_rate = 4 * 44100

listening = average_listening
excitement_point = np.array([64, 28])

dampening_per_second = 0.5
spring_strength = sample_rate * 600
min_mass = 1
max_mass = 0.01

spatial_step = 4
````
[combination_2024_04_23-11_02_03.mp4](results%2Fphysical_modelling%2Fcombination_2024_04_23-11_02_03.mp4)
- Schwinung durch Anregung kommt nicht auf der rechten Seite an! (und auch nicht bei jedem Maximum)

[combination_2024_04_23-11_06_09.mp4](results%2Fphysical_modelling%2Fcombination_2024_04_23-11_06_09.mp4)
- Abtastung: Gewichteter Durchschnitt

[combination_2024_04_23-11_54_21.mp4](results%2Fphysical_modelling%2Fcombination_2024_04_23-11_54_21.mp4)
- Anregung: Rauschen durch Bewegung
- ````dampening_per_second = 0.9````
- Scheint nicht wirklich unterschiedlich zu klingen.
- Auslenkungen sind fast gleichmäßig verteilt
- Rechte Hälft schwingt deutlich weniger als Linke

[combination_2024_04_23-12_03_07.mp4](results%2Fphysical_modelling%2Fcombination_2024_04_23-12_03_07.mp4)
- Anregung: Rauschen durch Bewegung
- ````dampening_per_second = 0.9````
- Abtastung: Gewichteter Durchschnitt

---

#### Sample Rate-Reduktion
- Laufende Simulation mit Dirac-Anregung und invertierten Massen
- Massenverteilung: Laufende Simulation (siehe min_mass, max_mass)
- Abtastung: Durchschnitt
- Anregung direkt auf der Glockenkurve
- 1 zu 1 Samplerate!
- Langsameres Video
````
sample_rate = 44100

listening = average_listening
scaling = scaling_none
excitement_point = np.array([64, 28])

dampening_per_second = 0.5 # 1 - 1e-3
spring_strength = sample_rate * 1000
min_mass = 1
max_mass = 0.01

spatial_step = 4
````

[combination_2024_04_24-10_23_58.mp4](results%2Fphysical_modelling%2Fcombination_2024_04_24-10_23_58.mp4)