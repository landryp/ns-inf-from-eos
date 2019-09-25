# ns-inf-from-eos
Code for inference of neutron star properties from EoS posterior samples.

_Dependencies: [ns-struc](https://github.com/landryp/ns-struc), [phenom-eos](https://github.com/landryp/phenom-eos)_

---

### Scripts

###### Generate prior samples from specified distributions

* makepriorsamples varname distr param1,param2,... -v -n numsamps -o path/to/output/dir/

###### Extrapolate binary neutron star spins to merger

* getspinatmerger spin Tc tau -v

###### Infer moment of inertia and spin, plus effective spin for a binary

* inferspin nsname path/to/macro/props/dir/ path/to/m/prior/samples.csv path/to/f/prior/samples.csv -v -n nummcsamps -o path/to/output/dir/

* inferchieff nsname path/to/macro/props/dir/ path/to/m1/prior/samples.csv path/to/m2/prior/samples.csv path/to/f1/prior/samples.csv path/to/f2/prior/samples.csv path/to/costheta1/prior/samples.csv path/to/costheta2/prior/samples.csv -v -n nummcsamps -o path/to/output/dir/

###### Infer tidal deformability, radius and compactness

* inferradius nsname path/to/macro/props/dir/ path/to/m/prior/samples.csv -v -n nummcsamps -o path/to/output/dir/

###### Calculate confidence intervals

* calcintervals postsamps.csv -v -p I,chi -L conflvl -d path/to/post/samples/dir/ -o path/to/output/dir/

---

### Tools

###### Make histogram of single observable

* plothist priorsamps.csv,postsamps.csv -x var -l xmin,xmax -d path/to/samples/dir/ -o path/to/output/dir/

###### Make corner plot of several observables

* plotcorner priorsamps.csv,postsamps.csv -x var1,var2,... -l x1min,x1max,x2min,x2max,... -d path/to/samples/dir/ -o path/to/output/dir/

---

### Instructions for performing inference

Take LVC's GW170817 spectral EoS posterior [samples](https://dcc.ligo.org/public/0152/P1800115/012/Parametrized-EoS_maxmass_EoS_samples.dat) as input.

###### Generate spectral EoSs from samples

* makespec path/to/samples.csv path/to/output/dir/

* addcrusts path/to/input/dir/ path/to/output/dir/

* getnsprops $(find path/to/input/dir/*cr.csv -type f -printf "%f,") -p R,M,I,Lambda -d path/to/input/dir/ -o path/to/output/dir/

###### Infer spin for target pulsar

* inferspin nsname path/to/macro/dir/ path/to/m/prior/samples path/to/f/prior/samples -o path/to/output/dir/

* plothist path/to/post.csv -x chi -o path/to/output/dir/ -b numbins -t _chi

* calcintervals nsname_spin.csv -v -p I,chi -L conflvl -d path/to/post.csv -o path/to/output/dir

###### Infer effective spin for target binary pulsar

* inferchieff nsname path/to/macro/dir/ path/to/m1/prior/samples path/to/m2/prior/samples path/to/f1/prior/samples path/to/f2/prior/samples path/to/costheta1/prior/samples path/to/costheta2/prior/samples -o path/to/output/dir/

* plotcorner path/to/post.csv -x chi1,chi2,chieff -o path/to/output/dir/ -b numbins -t _chieff

* calcintervals nsname_chieff.csv -v -p I,chi,chieff -L conflvl -d path/to/post.csv -o path/to/output/dir

