# -*- coding: utf-8 -*-
"""Section VIII: the quantum interface."""

SEC_VIII = '''
<h2>VIII. The quantum interface</h2>

<h3>A. The question, stated so that it can be answered</h3>

<p>A weight vector is a probability distribution, and a probability distribution is
the diagonal of a density matrix. The temptation is to read the fusion formula as a
quantum statement and to speak of amplitudes, superpositions and speed-ups. That
reading has to be resisted or made precise, and there are three ways to make it
precise. Either (a) the construction applies to quantum objects as well as classical
ones; or (b) the weights are <i>estimated from</i> quantum measurements, and the
formula itself is classical throughout; or (c) the connection is a metaphor. The third
needs no mathematics. The second is the reading I develop, because it is well posed,
it has content, and it produces the certificates of Section VII. The first is the
interesting one, and the answer is a one-directional theorem with a counterexample at
the other end.</p>

<h3>B. The commuting case, which is exact</h3>

<p>Let <i>p</i> be a weight vector and consider the diagonal state
&rho; = diag(<i>p</i>). For two such states the trace distance reduces to total
variation, the von Neumann entropy reduces to the Shannon entropy, and the Helstrom
error reduces to a statement about score ranges. All three facts are elementary and
all three are the hinge of what follows.</p>

<p><span class="t">Lemma 2 (diagonal states).</span> For probability vectors
<i>p</i>, <i>q</i>: &frac12;&Vert;&rho;&minus;&sigma;&Vert;<sub>1</sub> =
&frac12;&Vert;<i>p</i>&minus;<i>q</i>&Vert;<sub>1</sub> = TV(<i>p</i>,<i>q</i>); the
von Neumann entropy of &rho; equals the Shannon entropy of <i>p</i>; and the minimum
error probability in distinguishing &rho; from &sigma; with equal priors is
(1&minus;TV)/2.</p>

<p><i>Proof.</i> The difference of two diagonal matrices is diagonal, so its singular
values are the moduli of its diagonal entries, giving the distance identity; the
entropy claim is the definition evaluated on the spectrum; and the Helstrom expression
for two states with equal priors is (1&minus;&frac12;&Vert;&rho;&minus;&sigma;&Vert;<sub>1</sub>)/2
[5]. Appendix A.9 collects the details and the standard citations. &#9633;</p>

<p>Lemma 2 licenses a precise statement about the classical theory: everything in
Sections III to VII is the commuting special case of a quantum statement. That is a
compliment rather than a diminishment, and it tells the implementer what the weights
<i>are</i> in quantum language &mdash; the diagonal of a density matrix.</p>

<h3>C. The bound that survives</h3>

<div class="thm">
<p><span class="t">Theorem 11 (dephasing is a contraction).</span></p>
<div class="body">
<p>Let &Delta; denote complete dephasing in the computational basis,
&Delta;(&rho;) = diag(&rho;). For density matrices &rho;, &sigma; of the same
dimension,</p>
<div class="eq">
TV(&Delta;(&rho;), &Delta;(&sigma;)) &le; TV(&rho;, &sigma;).
<span class="num">(13)</span>
</div>
<p>Consequently a classical computation on the diagonals is a <i>lower bound</i>: it
can understate how distinguishable two states are, never overstate it.</p>
</div>
</div>

<p><i>Proof.</i> &Delta; is the pinching with respect to the computational-basis
projection family. A pinching is trace-preserving and completely positive, and it does
not increase the trace norm: &Vert;&Delta;(<i>X</i>)&Vert;<sub>1</sub> &le;
&Vert;<i>X</i>&Vert;<sub>1</sub> for every trace-class <i>X</i> [6, 4]. Applying this
to <i>X</i> = &rho;&minus;&sigma; and halving gives (13). &#9633;</p>

<p>Theorem 11 is the honest form of a quantum claim about this construction. If the
weights are measured from a quantum state, every number the classical pipeline computes
is a lower bound on the corresponding quantum distinguishability: the pipeline may say
two states are close when a measurement could tell them apart, and never the reverse.
For a decision system that is the right direction of error, because it means the
classical summary is conservative with respect to the quantum information it
discards.</p>

<figure>
<img src="figures/fig7_trace_distance.svg" alt="diagonal against full trace distance"/>
<figcaption><b>Figure 7.</b> Trace distance of the dephased states (horizontal) against
trace distance of the full states (vertical), over 250 random pairs of density matrices
of dimension up to five. Every point lies on or above the identity line, which is
Theorem 11; the vertical distance to the line is the contribution of coherence, and it
is large &mdash; here the mean coherence contribution is 0.314 against a mean diagonal
component of 0.248. Coherence is not a rounding error in the distinguishability budget.
Source: <i>results/e11_dephasing.json</i>.</figcaption>
</figure>

<h3>D. The bound that does not survive, and why</h3>

<p>The natural next hope is a converse: that the diagonal determines the distance, so
that the classical computation is not only a lower bound but a sufficient statistic. It
is false, and two lines settle it.</p>

<div class="thm">
<p><span class="t">Theorem 12 (no converse).</span></p>
<div class="body">
<p>There exist orthogonal pure states &rho; &ne; &sigma; with
&Delta;(&rho;) = &Delta;(&sigma;). Hence TV(&Delta;(&rho;),&Delta;(&sigma;)) = 0 while
TV(&rho;,&sigma;) = 1, and no function of the diagonals can certify a distance between
coherent states.</p>
</div>
</div>

<p><i>Proof.</i> Take |&psi;&rang; = &frac12;(1,1,1,1)<sup>&#8868;</sup> and
|&phi;&rang; = &frac12;(1,1,&minus;1,&minus;1)<sup>&#8868;</sup>. Both have diagonal
entries &frac14;, so the dephased states coincide, while
&lang;&psi;|&phi;&rang; = 0, so the pure states are orthogonal and their trace distance
is 1. Appendix A.10 verifies the same statement numerically in double precision.
&#9633;</p>

<p>The experiment adds something more useful than the counterexample alone: over 200
random pairs of pure states with equal diagonals, all 200 had non-zero trace distance,
with mean 0.749 and maximum 0.998 (<i>results/e5_quantum_boundary.json</i>). The gap is
not a measure-zero pathology. The same experiment reports a quantitative inequality
that does survive: for pure states,
TV<sup>2</sup> &ge; 1 &minus; (&sum;<sub><i>i</i></sub>&radic;(<i>p<sub>i</sub>q<sub>i</sub></i>))<sup>2</sup>,
where <i>p</i>, <i>q</i> are the diagonals; the minimum excess over 200 random pairs
was 8.6&times;10<sup>&minus;5</sup>. The diagonal quantity is the fidelity of the
dephased states, which upper-bounds the fidelity of the states themselves, and that is
the reason the inequality points the way it does.</p>

<h3>E. A floor on the error probability</h3>

<p>For the decision-theoretic reading of a pipeline the quantity of interest is not the
distance but the error probability of a test. For weights obtained from scores
differing by a vector of range &Delta;, the companion report established
TV &le; tanh(|&beta;|&Delta;/4) [1]; the sharp form of that bound via the Hilbert metric
is due to Cohen and Fausti [10] and is used in the same form by Somasundaram et al.
[11]. Composing it with Lemma 2 gives a floor.</p>

<p><span class="t">Corollary 1 (Helstrom floor).</span> Let two diagonal states have
weights obtained from scores differing by a vector of range &Delta;. Then the minimum
error probability of distinguishing them with equal priors satisfies</p>

<div class="eq">
P<sub>e</sub> &ge; (1 &minus; tanh(|&beta;|&Delta;/4))/2.
<span class="num">(14)</span>
</div>

<p>Figure 8 plots the floor for four temperatures, and
<i>results/e6_helstrom.json</i> reports 400 random cases in which the measured Helstrom
error never fell below it: the smallest slack was 1.2&times;10<sup>&minus;5</sup> and the
mean slack rose with &beta; from 0.040 at &beta; = 0.5 to 0.235 at &beta; = 8. The mean
slack is worth a remark: the floor is loose precisely where the pipeline is sharp, which
is the regime a practitioner cares about. A loose bound is still a bound, but (14)
should not be mistaken for an estimate.</p>

<figure>
<img src="figures/fig8_helstrom.svg" alt="Helstrom floor curves"/>
<figcaption><b>Figure 8.</b> The lower bound (14) on the error probability of
distinguishing two diagonal states whose scores differ by a vector of range &Delta;, for
four values of &beta;. The bound decays with the range and rises with &beta;; it is
never tight, and its value is that it forbids any claim of distinguishability below the
curve.</figcaption>
</figure>

<h3>F. What the quantum reading delivers, and what it does not</h3>

<p>Four sentences, written plainly rather than left to inference. A Gibbs weight vector
is the diagonal of a density matrix, and in that reading the whole classical theory is
the commuting special case. If a device prepares states whose diagonals are the weights,
estimating those weights by measurement is a well-posed statistical problem and
Theorem 10 applies with the shot count equal to the number of measurements. Coherence
adds distinguishability that the diagonal cannot see, in one direction only, so a
classical pipeline built on weights is conservative. And nothing in this section implies
that a quantum device computes the fusion faster, or that the formula is a quantum
algorithm: the formula has no amplitudes, no unitaries and no interference, and calling
it a quantum algorithm would be a claim its own mathematics contradicts.</p>

<p>One constructive consequence is worth naming. Because the weights are a diagonal, the
preparation problem is a state-preparation problem of a specific and well-studied shape:
produce a state whose computational-basis distribution is the Gibbs distribution of the
scores. The certificate then does double duty, bounding the error induced by finite
measurements regardless of how the state was produced, which means a pipeline can accept
weights from a quantum device, a classical sampler, or a validation set and treat them
identically. That interchangeability is the only sense in which I am willing to attach
the word quantum to this mathematics, and it is a smaller claim than the word usually
carries.</p>
'''
