/* Created by Language version: 7.7.0 */
/* NOT VECTORIZED */
#define NRN_VECTORIZED 0
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "mech_api.h"
#undef PI
#define nil 0
#define _pval pval
// clang-format off
#include "md1redef.h"
#include "section_fwd.hpp"
#include "nrniv_mf.h"
#include "md2redef.h"
#include "nrnconf.h"
// clang-format on
#include "neuron/cache/mechanism_range.hpp"
#include <vector>
using std::size_t;
static auto& std_cerr_stream = std::cerr;
static constexpr auto number_of_datum_variables = 5;
static constexpr auto number_of_floating_point_variables = 9;
namespace {
template <typename T>
using _nrn_mechanism_std_vector = std::vector<T>;
using _nrn_model_sorted_token = neuron::model_sorted_token;
using _nrn_mechanism_cache_range = neuron::cache::MechanismRange<number_of_floating_point_variables, number_of_datum_variables>;
using _nrn_mechanism_cache_instance = neuron::cache::MechanismInstance<number_of_floating_point_variables, number_of_datum_variables>;
using _nrn_non_owning_id_without_container = neuron::container::non_owning_identifier_without_container;
template <typename T>
using _nrn_mechanism_field = neuron::mechanism::field<T>;
template <typename... Args>
void _nrn_mechanism_register_data_fields(Args&&... args) {
  neuron::mechanism::register_data_fields(std::forward<Args>(args)...);
}
}
 
#if !NRNGPU
#undef exp
#define exp hoc_Exp
#if NRN_ENABLE_ARCH_INDEP_EXP_POW
#undef pow
#define pow hoc_pow
#endif
#endif
 
#define nrn_init _nrn_init__kca3
#define _nrn_initial _nrn_initial__kca3
#define nrn_cur _nrn_cur__kca3
#define _nrn_current _nrn_current__kca3
#define nrn_jacob _nrn_jacob__kca3
#define nrn_state _nrn_state__kca3
#define _net_receive _net_receive__kca3 
#define _f_concdep _f_concdep__kca3 
#define _f_vdep _f_vdep__kca3 
#define concdep concdep__kca3 
#define rate rate__kca3 
#define state state__kca3 
#define vdep vdep__kca3 
 
#define _threadargscomma_ /**/
#define _threadargsprotocomma_ /**/
#define _internalthreadargsprotocomma_ /**/
#define _threadargs_ /**/
#define _threadargsproto_ /**/
#define _internalthreadargsproto_ /**/
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *hoc_getarg(int);
 
#define t nrn_threads->_t
#define dt nrn_threads->_dt
#define gkbar _ml->template fpfield<0>(_iml)
#define gkbar_columnindex 0
#define ik _ml->template fpfield<1>(_iml)
#define ik_columnindex 1
#define Yvdep _ml->template fpfield<2>(_iml)
#define Yvdep_columnindex 2
#define Yconcdep _ml->template fpfield<3>(_iml)
#define Yconcdep_columnindex 3
#define Y _ml->template fpfield<4>(_iml)
#define Y_columnindex 4
#define ek _ml->template fpfield<5>(_iml)
#define ek_columnindex 5
#define cai _ml->template fpfield<6>(_iml)
#define cai_columnindex 6
#define DY _ml->template fpfield<7>(_iml)
#define DY_columnindex 7
#define _g _ml->template fpfield<8>(_iml)
#define _g_columnindex 8
#define _ion_ek *(_ml->dptr_field<0>(_iml))
#define _p_ion_ek static_cast<neuron::container::data_handle<double>>(_ppvar[0])
#define _ion_ik *(_ml->dptr_field<1>(_iml))
#define _p_ion_ik static_cast<neuron::container::data_handle<double>>(_ppvar[1])
#define _ion_dikdv *(_ml->dptr_field<2>(_iml))
#define _ion_cai *(_ml->dptr_field<3>(_iml))
#define _p_ion_cai static_cast<neuron::container::data_handle<double>>(_ppvar[3])
#define _ion_cao *(_ml->dptr_field<4>(_iml))
#define _p_ion_cao static_cast<neuron::container::data_handle<double>>(_ppvar[4])
 static _nrn_mechanism_cache_instance _ml_real{nullptr};
static _nrn_mechanism_cache_range *_ml{&_ml_real};
static size_t _iml{0};
static Datum *_ppvar;
 static int hoc_nrnpointerindex =  -1;
 static Prop* _extcall_prop;
 /* _prop_id kind of shadows _extcall_prop to allow validity checking. */
 static _nrn_non_owning_id_without_container _prop_id{};
 /* external NEURON variables */
 /* declaration of user functions */
 static void _hoc_concdep(void);
 static void _hoc_rate(void);
 static void _hoc_vdep(void);
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
 
#define NMODL_TEXT 1
#if NMODL_TEXT
static void register_nmodl_text_and_filename(int mechtype);
#endif
 static void _hoc_setdata();
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 {"setdata_kca3", _hoc_setdata},
 {"concdep_kca3", _hoc_concdep},
 {"rate_kca3", _hoc_rate},
 {"vdep_kca3", _hoc_vdep},
 {0, 0}
};
 
/* Direct Python call wrappers to density mechanism functions.*/
 static double _npy_concdep(Prop*);
 static double _npy_rate(Prop*);
 static double _npy_vdep(Prop*);
 
static NPyDirectMechFunc npy_direct_func_proc[] = {
 {"concdep", _npy_concdep},
 {"rate", _npy_rate},
 {"vdep", _npy_vdep},
 {0, 0}
};
 /* declare global and static user variables */
 #define gind 0
 #define _gth 0
#define Ybeta Ybeta_kca3
 double Ybeta = 0.05;
#define Yalpha Yalpha_kca3
 double Yalpha = 0;
#define usetable usetable_kca3
 double usetable = 1;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 {"gkbar_kca3", 0, 1e+09},
 {"usetable_kca3", 0, 1},
 {0, 0, 0}
};
 static HocParmUnits _hoc_parm_units[] = {
 {"Ybeta_kca3", "/ms"},
 {"Yalpha_kca3", "/ms"},
 {"gkbar_kca3", "mho/cm2"},
 {"ik_kca3", "mA/cm2"},
 {"Yconcdep_kca3", "/ms"},
 {0, 0}
};
 static double Y0 = 0;
 static double delta_t = 0.01;
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 {"Ybeta_kca3", &Ybeta_kca3},
 {"Yalpha_kca3", &Yalpha_kca3},
 {"usetable_kca3", &usetable_kca3},
 {0, 0}
};
 static DoubVec hoc_vdoub[] = {
 {0, 0, 0}
};
 static double _sav_indep;
 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _extcall_prop = _prop;
 _prop_id = _nrn_get_prop_id(_prop);
 neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
_ppvar = _nrn_mechanism_access_dparam(_prop);
 Node * _node = _nrn_mechanism_access_node(_prop);
v = _nrn_mechanism_access_voltage(_node);
 }
 static void _hoc_setdata() {
 Prop *_prop, *hoc_getdata_range(int);
 _prop = hoc_getdata_range(_mechtype);
   _setdata(_prop);
 hoc_retpushx(1.);
}
 static void nrn_alloc(Prop*);
static void nrn_init(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
static void nrn_state(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
 static void nrn_cur(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
static void nrn_jacob(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
 
static int _ode_count(int);
static void _ode_map(Prop*, int, neuron::container::data_handle<double>*, neuron::container::data_handle<double>*, double*, int);
static void _ode_spec(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
static void _ode_matsol(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
 
#define _cvode_ieq _ppvar[5].literal_value<int>()
 static void _ode_matsol_instance1(_internalthreadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"kca3",
 "gkbar_kca3",
 0,
 "ik_kca3",
 "Yvdep_kca3",
 "Yconcdep_kca3",
 0,
 "Y_kca3",
 0,
 0};
 static Symbol* _k_sym;
 static Symbol* _ca_sym;
 
 /* Used by NrnProperty */
 static _nrn_mechanism_std_vector<double> _parm_default{
     0.12, /* gkbar */
 }; 
 
 
extern Prop* need_memb(Symbol*);
static void nrn_alloc(Prop* _prop) {
  Prop *prop_ion{};
  Datum *_ppvar{};
   _ppvar = nrn_prop_datum_alloc(_mechtype, 6, _prop);
    _nrn_mechanism_access_dparam(_prop) = _ppvar;
     _nrn_mechanism_cache_instance _ml_real{_prop};
    auto* const _ml = &_ml_real;
    size_t const _iml{};
    assert(_nrn_mechanism_get_num_vars(_prop) == 9);
 	/*initialize range parameters*/
 	gkbar = _parm_default[0]; /* 0.12 */
 	 assert(_nrn_mechanism_get_num_vars(_prop) == 9);
 	_nrn_mechanism_access_dparam(_prop) = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_k_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[0] = _nrn_mechanism_get_param_handle(prop_ion, 0); /* ek */
 	_ppvar[1] = _nrn_mechanism_get_param_handle(prop_ion, 3); /* ik */
 	_ppvar[2] = _nrn_mechanism_get_param_handle(prop_ion, 4); /* _ion_dikdv */
 prop_ion = need_memb(_ca_sym);
 nrn_promote(prop_ion, 1, 0);
 	_ppvar[3] = _nrn_mechanism_get_param_handle(prop_ion, 1); /* cai */
 	_ppvar[4] = _nrn_mechanism_get_param_handle(prop_ion, 2); /* cao */
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 {0, 0}
};
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
void _nrn_thread_table_reg(int, nrn_thread_table_check_t);
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 extern "C" void _kca3_reg() {
	int _vectorized = 0;
  _initlists();
 	ion_reg("k", -10000.);
 	ion_reg("ca", -10000.);
 	_k_sym = hoc_lookup("k_ion");
 	_ca_sym = hoc_lookup("ca_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 0);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
 hoc_register_parm_default(_mechtype, &_parm_default);
         hoc_register_npy_direct(_mechtype, npy_direct_func_proc);
     _nrn_setdata_reg(_mechtype, _setdata);
 #if NMODL_TEXT
  register_nmodl_text_and_filename(_mechtype);
#endif
   _nrn_mechanism_register_data_fields(_mechtype,
                                       _nrn_mechanism_field<double>{"gkbar"} /* 0 */,
                                       _nrn_mechanism_field<double>{"ik"} /* 1 */,
                                       _nrn_mechanism_field<double>{"Yvdep"} /* 2 */,
                                       _nrn_mechanism_field<double>{"Yconcdep"} /* 3 */,
                                       _nrn_mechanism_field<double>{"Y"} /* 4 */,
                                       _nrn_mechanism_field<double>{"ek"} /* 5 */,
                                       _nrn_mechanism_field<double>{"cai"} /* 6 */,
                                       _nrn_mechanism_field<double>{"DY"} /* 7 */,
                                       _nrn_mechanism_field<double>{"_g"} /* 8 */,
                                       _nrn_mechanism_field<double*>{"_ion_ek", "k_ion"} /* 0 */,
                                       _nrn_mechanism_field<double*>{"_ion_ik", "k_ion"} /* 1 */,
                                       _nrn_mechanism_field<double*>{"_ion_dikdv", "k_ion"} /* 2 */,
                                       _nrn_mechanism_field<double*>{"_ion_cai", "ca_ion"} /* 3 */,
                                       _nrn_mechanism_field<double*>{"_ion_cao", "ca_ion"} /* 4 */,
                                       _nrn_mechanism_field<int>{"_cvode_ieq", "cvodeieq"} /* 5 */);
  hoc_register_prop_size(_mechtype, 9, 6);
  hoc_register_dparam_semantics(_mechtype, 0, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 5, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 
    hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 kca3 /home/rj/projects/temp/temp/CAMP/project_3.1/2487-master/kca3.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double *_t_Yvdep;
 static double *_t_Yconcdep;
static int _reset;
static const char *modelname = "Calcium dependent potassium channel";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int _f_concdep(double);
static int _f_vdep(double);
static int concdep(double);
static int rate(double, double);
static int vdep(double);
 
static int _ode_spec1(_internalthreadargsproto_);
/*static int _ode_matsol1(_internalthreadargsproto_);*/
 static void _n_concdep(double);
 static void _n_vdep(double);
 static neuron::container::field_index _slist1[1], _dlist1[1];
 static int state(_internalthreadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 () {_reset=0;
 {
   rate ( _threadargscomma_ v , cai ) ;
   DY = Yalpha * ( 1.0 - Y ) - Ybeta * Y ;
   }
 return _reset;
}
 static int _ode_matsol1 () {
 rate ( _threadargscomma_ v , cai ) ;
 DY = DY  / (1. - dt*( ( Yalpha )*( ( ( - 1.0 ) ) ) - ( Ybeta )*( 1.0 ) )) ;
  return 0;
}
 /*END CVODE*/
 static int state () {_reset=0;
 {
   rate ( _threadargscomma_ v , cai ) ;
    Y = Y + (1. - exp(dt*(( Yalpha )*( ( ( - 1.0 ) ) ) - ( Ybeta )*( 1.0 ))))*(- ( ( Yalpha )*( ( 1.0 ) ) ) / ( ( Yalpha )*( ( ( - 1.0 ) ) ) - ( Ybeta )*( 1.0 ) ) - Y) ;
   }
  return 0;
}
 
static int  rate (  double _lv , double _lcai ) {
   vdep ( _threadargscomma_ _lv ) ;
   concdep ( _threadargscomma_ _lcai ) ;
   Yalpha = Yvdep * Yconcdep ;
    return 0; }
 
static void _hoc_rate(void) {
  double _r;
  
  if(!_prop_id) {
    hoc_execerror("No data for rate_kca3. Requires prior call to setdata_kca3 and that the specified mechanism instance still be in existence.", NULL);
  } else {
    _setdata(_extcall_prop);
  }
   _r = 1.;
 rate (  *getarg(1) , *getarg(2) );
 hoc_retpushx(_r);
}
 
static double _npy_rate(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r = 1.;
 rate (  *getarg(1) , *getarg(2) );
 return(_r);
}
 static double _mfac_vdep, _tmin_vdep;
 static void _check_vdep();
 static void _check_vdep() {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  if (!usetable) {return;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_vdep =  - 100.0 ;
   _tmax =  100.0 ;
   _dx = (_tmax - _tmin_vdep)/100.; _mfac_vdep = 1./_dx;
   for (_i=0, _x=_tmin_vdep; _i < 101; _x += _dx, _i++) {
    _f_vdep(_x);
    _t_Yvdep[_i] = Yvdep;
   }
  }
 }

 static int vdep(double _lv){ _check_vdep();
 _n_vdep(_lv);
 return 0;
 }

 static void _n_vdep(double _lv){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 _f_vdep(_lv); return; 
}
 _xi = _mfac_vdep * (_lv - _tmin_vdep);
 if (std::isnan(_xi)) {
  Yvdep = _xi;
  return;
 }
 if (_xi <= 0.) {
 Yvdep = _t_Yvdep[0];
 return; }
 if (_xi >= 100.) {
 Yvdep = _t_Yvdep[100];
 return; }
 _i = (int) _xi;
 _theta = _xi - (double)_i;
 Yvdep = _t_Yvdep[_i] + _theta*(_t_Yvdep[_i+1] - _t_Yvdep[_i]);
 }

 
static int  _f_vdep (  double _lv ) {
   Yvdep = exp ( ( _lv * 1.0 + 70.0 ) / 27.0 ) ;
    return 0; }
 
static void _hoc_vdep(void) {
  double _r;
  
  if(!_prop_id) {
    hoc_execerror("No data for vdep_kca3. Requires prior call to setdata_kca3 and that the specified mechanism instance still be in existence.", NULL);
  } else {
    _setdata(_extcall_prop);
  }
    _r = 1.;
 vdep (  *getarg(1) );
 hoc_retpushx(_r);
}
 
static double _npy_vdep(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
  _r = 1.;
 vdep (  *getarg(1) );
 return(_r);
}
 static double _mfac_concdep, _tmin_concdep;
 static void _check_concdep();
 static void _check_concdep() {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  if (!usetable) {return;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_concdep =  0.0 ;
   _tmax =  0.01 ;
   _dx = (_tmax - _tmin_concdep)/1000.; _mfac_concdep = 1./_dx;
   for (_i=0, _x=_tmin_concdep; _i < 1001; _x += _dx, _i++) {
    _f_concdep(_x);
    _t_Yconcdep[_i] = Yconcdep;
   }
  }
 }

 static int concdep(double _lcai){ _check_concdep();
 _n_concdep(_lcai);
 return 0;
 }

 static void _n_concdep(double _lcai){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 _f_concdep(_lcai); return; 
}
 _xi = _mfac_concdep * (_lcai - _tmin_concdep);
 if (std::isnan(_xi)) {
  Yconcdep = _xi;
  return;
 }
 if (_xi <= 0.) {
 Yconcdep = _t_Yconcdep[0];
 return; }
 if (_xi >= 1000.) {
 Yconcdep = _t_Yconcdep[1000];
 return; }
 _i = (int) _xi;
 _theta = _xi - (double)_i;
 Yconcdep = _t_Yconcdep[_i] + _theta*(_t_Yconcdep[_i+1] - _t_Yconcdep[_i]);
 }

 
static int  _f_concdep (  double _lcai ) {
   if ( _lcai < 0.01 ) {
     Yconcdep = 500.0 * ( 0.015 - _lcai * 1.0 ) / ( exp ( ( 0.015 - _lcai * 1.0 ) / 0.0013 ) - 1.0 ) ;
     }
   else {
     Yconcdep = 500.0 * 0.005 / ( exp ( 0.005 / 0.0013 ) - 1.0 ) ;
     }
    return 0; }
 
static void _hoc_concdep(void) {
  double _r;
  
  if(!_prop_id) {
    hoc_execerror("No data for concdep_kca3. Requires prior call to setdata_kca3 and that the specified mechanism instance still be in existence.", NULL);
  } else {
    _setdata(_extcall_prop);
  }
    _r = 1.;
 concdep (  *getarg(1) );
 hoc_retpushx(_r);
}
 
static double _npy_concdep(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
  _r = 1.;
 concdep (  *getarg(1) );
 return(_r);
}
 
static int _ode_count(int _type){ return 1;}
 
static void _ode_spec(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type) {
      Node* _nd{};
  double _v{};
  int _cntml;
  _nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
  _ml = &_lmr;
  _cntml = _ml_arg->_nodecount;
  Datum *_thread{_ml_arg->_thread};
  double* _globals = nullptr;
  if (gind != 0 && _thread != nullptr) { _globals = _thread[_gth].get<double*>(); }
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _ppvar = _ml_arg->_pdata[_iml];
    _nd = _ml_arg->_nodelist[_iml];
    v = NODEV(_nd);
  ek = _ion_ek;
  cai = _ion_cai;
     _ode_spec1 ();
  }}
 
static void _ode_map(Prop* _prop, int _ieq, neuron::container::data_handle<double>* _pv, neuron::container::data_handle<double>* _pvdot, double* _atol, int _type) { 
  _ppvar = _nrn_mechanism_access_dparam(_prop);
  _cvode_ieq = _ieq;
  for (int _i=0; _i < 1; ++_i) {
    _pv[_i] = _nrn_mechanism_get_param_handle(_prop, _slist1[_i]);
    _pvdot[_i] = _nrn_mechanism_get_param_handle(_prop, _dlist1[_i]);
    _cvode_abstol(_atollist, _atol, _i);
  }
 }
 
static void _ode_matsol_instance1(_internalthreadargsproto_) {
 _ode_matsol1 ();
 }
 
static void _ode_matsol(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type) {
      Node* _nd{};
  double _v{};
  int _cntml;
  _nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
  _ml = &_lmr;
  _cntml = _ml_arg->_nodecount;
  Datum *_thread{_ml_arg->_thread};
  double* _globals = nullptr;
  if (gind != 0 && _thread != nullptr) { _globals = _thread[_gth].get<double*>(); }
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _ppvar = _ml_arg->_pdata[_iml];
    _nd = _ml_arg->_nodelist[_iml];
    v = NODEV(_nd);
  ek = _ion_ek;
  cai = _ion_cai;
 _ode_matsol_instance1(_threadargs_);
 }}

static void initmodel() {
  int _i; double _save;_ninits++;
 _save = t;
 t = 0.0;
{
  Y = Y0;
 {
   rate ( _threadargscomma_ v , cai ) ;
   Y = Yalpha / ( Yalpha + Ybeta ) ;
   }
  _sav_indep = t; t = _save;

}
}

static void nrn_init(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type){
Node *_nd; double _v; int* _ni; int _cntml;
_nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
auto* const _vec_v = _nt->node_voltage_storage();
_ml = &_lmr;
_ni = _ml_arg->_nodeindices;
_cntml = _ml_arg->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _ppvar = _ml_arg->_pdata[_iml];
   _v = _vec_v[_ni[_iml]];
 v = _v;
  ek = _ion_ek;
  cai = _ion_cai;
 initmodel();
 }}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
   ik = gkbar * Y * ( v - ek ) ;
   }
 _current += ik;

} return _current;
}

static void nrn_cur(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type){
_nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
auto const _vec_rhs = _nt->node_rhs_storage();
auto const _vec_sav_rhs = _nt->node_sav_rhs_storage();
auto const _vec_v = _nt->node_voltage_storage();
Node *_nd; int* _ni; double _rhs, _v; int _cntml;
_ml = &_lmr;
_ni = _ml_arg->_nodeindices;
_cntml = _ml_arg->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _ppvar = _ml_arg->_pdata[_iml];
   _v = _vec_v[_ni[_iml]];
  ek = _ion_ek;
  cai = _ion_cai;
 auto const _g_local = _nrn_current(_v + .001);
 	{ double _dik;
  _dik = ik;
 _rhs = _nrn_current(_v);
  _ion_dikdv += (_dik - ik)/.001 ;
 	}
 _g = (_g_local - _rhs)/.001;
  _ion_ik += ik ;
	 _vec_rhs[_ni[_iml]] -= _rhs;
 
}}

static void nrn_jacob(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type) {
_nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
auto const _vec_d = _nt->node_d_storage();
auto const _vec_sav_d = _nt->node_sav_d_storage();
auto* const _ml = &_lmr;
Node *_nd; int* _ni; int _iml, _cntml;
_ni = _ml_arg->_nodeindices;
_cntml = _ml_arg->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
  _vec_d[_ni[_iml]] += _g;
 
}}

static void nrn_state(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type){
Node *_nd; double _v = 0.0; int* _ni; int _cntml;
_nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
auto* const _vec_v = _nt->node_voltage_storage();
_ml = &_lmr;
_ni = _ml_arg->_nodeindices;
_cntml = _ml_arg->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _ppvar = _ml_arg->_pdata[_iml];
 _nd = _ml_arg->_nodelist[_iml];
   _v = _vec_v[_ni[_iml]];
 v=_v;
{
  ek = _ion_ek;
  cai = _ion_cai;
 { error =  state();
 if(error){
  std_cerr_stream << "at line 51 in file kca3.mod:\nBREAKPOINT {\n";
  std_cerr_stream << _ml << ' ' << _iml << '\n';
  abort_run(error);
}
 } }}

}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = {Y_columnindex, 0};  _dlist1[0] = {DY_columnindex, 0};
   _t_Yvdep = makevector(101*sizeof(double));
   _t_Yconcdep = makevector(1001*sizeof(double));
_first = 0;
}

#if NMODL_TEXT
static void register_nmodl_text_and_filename(int mech_type) {
    const char* nmodl_filename = "/home/rj/projects/temp/temp/CAMP/project_3.1/2487-master/kca3.mod";
    const char* nmodl_file_text = 
  "TITLE Calcium dependent potassium channel\n"
  ": KCa channel with parameters from US Bhalla and JM Bower,\n"
  ": J. Neurophysiol. 69:1948-1983 (1993)\n"
  ": Adapted from /usr/local/neuron/demo/release/nachan.mod - squid\n"
  ": by Andrew Davison, The Babraham Institute.\n"
  ": 24-08-98\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX kca3\n"
  "	USEION k READ ek WRITE ik\n"
  "	USEION ca READ cai\n"
  "	RANGE gkbar, ik, Yconcdep, Yvdep\n"
  "	GLOBAL Yalpha, Ybeta\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	(mA) = (milliamp)\n"
  "	(mV) = (millivolt)\n"
  "	(molar) = (1/liter)\n"
  "	(mM) = (millimolar)\n"
  "}\n"
  "\n"
  "INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}\n"
  "\n"
  "PARAMETER {\n"
  "	v (mV)\n"
  "	dt (ms)\n"
  "	gkbar= 0.120 (mho/cm2) <0,1e9>\n"
  "	ek = -80 (mV)\n"
  "	Ybeta = 0.05 (/ms)\n"
  "	cai (mM) := 1e-5 (mM)\n"
  "}\n"
  "\n"
  "\n"
  "STATE {\n"
  "	Y\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	ik (mA/cm2)\n"
  "	Yalpha   (/ms)\n"
  "	Yvdep    \n"
  "	Yconcdep (/ms)\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "	rate(v,cai)\n"
  "	Y = Yalpha/(Yalpha + Ybeta)\n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "	SOLVE state METHOD cnexp\n"
  "	ik = gkbar*Y*(v - ek)\n"
  "}\n"
  "\n"
  "DERIVATIVE state {\n"
  "	rate(v,cai)\n"
  "	Y' = Yalpha*(1-Y) - Ybeta*Y\n"
  "}\n"
  "\n"
  "PROCEDURE rate(v(mV),cai(mM)) {\n"
  "	vdep(v)\n"
  "	concdep(cai)\n"
  "	Yalpha = Yvdep*Yconcdep\n"
  "}\n"
  "\n"
  "PROCEDURE vdep(v(mV)) {\n"
  "	TABLE Yvdep FROM -100 TO 100 WITH 100\n"
  "	Yvdep = exp((v*1(/mV)+70)/27)\n"
  "}\n"
  "\n"
  "PROCEDURE concdep(cai(mM)) {\n"
  "	TABLE Yconcdep FROM 0 TO 0.01 WITH 1000\n"
  "	if (cai < 0.01) {\n"
  "		Yconcdep = 500(/ms)*( 0.015-cai*1(/mM) )/( exp((0.015-cai*1(/mM))/0.0013) -1 )\n"
  "	} else {\n"
  "		Yconcdep = 500(/ms)*0.005/( exp(0.005/0.0013) -1 )\n"
  "	}\n"
  "}\n"
  ;
    hoc_reg_nmodl_filename(mech_type, nmodl_filename);
    hoc_reg_nmodl_text(mech_type, nmodl_file_text);
}
#endif
