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
static constexpr auto number_of_datum_variables = 2;
static constexpr auto number_of_floating_point_variables = 7;
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
 
#define nrn_init _nrn_init__lcafixed
#define _nrn_initial _nrn_initial__lcafixed
#define nrn_cur _nrn_cur__lcafixed
#define _nrn_current _nrn_current__lcafixed
#define nrn_jacob _nrn_jacob__lcafixed
#define nrn_state _nrn_state__lcafixed
#define _net_receive _net_receive__lcafixed 
#define _f_rates _f_rates__lcafixed 
#define rates rates__lcafixed 
#define states states__lcafixed 
 
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
#define gcabar _ml->template fpfield<0>(_iml)
#define gcabar_columnindex 0
#define ica _ml->template fpfield<1>(_iml)
#define ica_columnindex 1
#define r _ml->template fpfield<2>(_iml)
#define r_columnindex 2
#define s _ml->template fpfield<3>(_iml)
#define s_columnindex 3
#define Dr _ml->template fpfield<4>(_iml)
#define Dr_columnindex 4
#define Ds _ml->template fpfield<5>(_iml)
#define Ds_columnindex 5
#define _g _ml->template fpfield<6>(_iml)
#define _g_columnindex 6
#define _ion_ica *(_ml->dptr_field<0>(_iml))
#define _p_ion_ica static_cast<neuron::container::data_handle<double>>(_ppvar[0])
#define _ion_dicadv *(_ml->dptr_field<1>(_iml))
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
 static void _hoc_alp(void);
 static void _hoc_bet(void);
 static void _hoc_rates(void);
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
 {"setdata_lcafixed", _hoc_setdata},
 {"alp_lcafixed", _hoc_alp},
 {"bet_lcafixed", _hoc_bet},
 {"rates_lcafixed", _hoc_rates},
 {0, 0}
};
 
/* Direct Python call wrappers to density mechanism functions.*/
 static double _npy_alp(Prop*);
 static double _npy_bet(Prop*);
 static double _npy_rates(Prop*);
 
static NPyDirectMechFunc npy_direct_func_proc[] = {
 {"alp", _npy_alp},
 {"bet", _npy_bet},
 {"rates", _npy_rates},
 {0, 0}
};
#define alp alp_lcafixed
#define bet bet_lcafixed
 extern double alp( double , double );
 extern double bet( double , double );
 /* declare global and static user variables */
 #define gind 0
 #define _gth 0
#define rtau rtau_lcafixed
 double rtau = 0;
#define rinf rinf_lcafixed
 double rinf = 0;
#define stau stau_lcafixed
 double stau = 0;
#define sinf sinf_lcafixed
 double sinf = 0;
#define usetable usetable_lcafixed
 double usetable = 1;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 {"gcabar_lcafixed", 0, 1e+09},
 {"usetable_lcafixed", 0, 1},
 {0, 0, 0}
};
 static HocParmUnits _hoc_parm_units[] = {
 {"stau_lcafixed", "ms"},
 {"rtau_lcafixed", "ms"},
 {"gcabar_lcafixed", "mho/cm2"},
 {"ica_lcafixed", "mA/cm2"},
 {0, 0}
};
 static double delta_t = 0.01;
 static double r0 = 0;
 static double s0 = 0;
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 {"sinf_lcafixed", &sinf_lcafixed},
 {"rinf_lcafixed", &rinf_lcafixed},
 {"stau_lcafixed", &stau_lcafixed},
 {"rtau_lcafixed", &rtau_lcafixed},
 {"usetable_lcafixed", &usetable_lcafixed},
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
 
#define _cvode_ieq _ppvar[2].literal_value<int>()
 static void _ode_matsol_instance1(_internalthreadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"lcafixed",
 "gcabar_lcafixed",
 0,
 "ica_lcafixed",
 0,
 "r_lcafixed",
 "s_lcafixed",
 0,
 0};
 static Symbol* _ca_sym;
 
 /* Used by NrnProperty */
 static _nrn_mechanism_std_vector<double> _parm_default{
     0.12, /* gcabar */
 }; 
 
 
extern Prop* need_memb(Symbol*);
static void nrn_alloc(Prop* _prop) {
  Prop *prop_ion{};
  Datum *_ppvar{};
   _ppvar = nrn_prop_datum_alloc(_mechtype, 3, _prop);
    _nrn_mechanism_access_dparam(_prop) = _ppvar;
     _nrn_mechanism_cache_instance _ml_real{_prop};
    auto* const _ml = &_ml_real;
    size_t const _iml{};
    assert(_nrn_mechanism_get_num_vars(_prop) == 7);
 	/*initialize range parameters*/
 	gcabar = _parm_default[0]; /* 0.12 */
 	 assert(_nrn_mechanism_get_num_vars(_prop) == 7);
 	_nrn_mechanism_access_dparam(_prop) = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_ca_sym);
 	_ppvar[0] = _nrn_mechanism_get_param_handle(prop_ion, 3); /* ica */
 	_ppvar[1] = _nrn_mechanism_get_param_handle(prop_ion, 4); /* _ion_dicadv */
 
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

 extern "C" void _lcafixed_reg() {
	int _vectorized = 0;
  _initlists();
 	ion_reg("ca", -10000.);
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
                                       _nrn_mechanism_field<double>{"gcabar"} /* 0 */,
                                       _nrn_mechanism_field<double>{"ica"} /* 1 */,
                                       _nrn_mechanism_field<double>{"r"} /* 2 */,
                                       _nrn_mechanism_field<double>{"s"} /* 3 */,
                                       _nrn_mechanism_field<double>{"Dr"} /* 4 */,
                                       _nrn_mechanism_field<double>{"Ds"} /* 5 */,
                                       _nrn_mechanism_field<double>{"_g"} /* 6 */,
                                       _nrn_mechanism_field<double*>{"_ion_ica", "ca_ion"} /* 0 */,
                                       _nrn_mechanism_field<double*>{"_ion_dicadv", "ca_ion"} /* 1 */,
                                       _nrn_mechanism_field<int>{"_cvode_ieq", "cvodeieq"} /* 2 */);
  hoc_register_prop_size(_mechtype, 7, 3);
  hoc_register_dparam_semantics(_mechtype, 0, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 
    hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 lcafixed /Users/shraddhapathak/Downloads/2487-master/lcafixed.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double eca = 70;
 static double *_t_sinf;
 static double *_t_rinf;
 static double *_t_stau;
 static double *_t_rtau;
static int _reset;
static const char *modelname = "LCa calcium channel with fixed reversal potential";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int _f_rates(double);
static int rates(double);
 
static int _ode_spec1(_internalthreadargsproto_);
/*static int _ode_matsol1(_internalthreadargsproto_);*/
 static void _n_rates(double);
 static neuron::container::field_index _slist1[2], _dlist1[2];
 static int states(_internalthreadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 () {_reset=0;
 {
   rates ( _threadargscomma_ v ) ;
   Ds = ( sinf - s ) / stau ;
   Dr = ( rinf - r ) / rtau ;
   }
 return _reset;
}
 static int _ode_matsol1 () {
 rates ( _threadargscomma_ v ) ;
 Ds = Ds  / (1. - dt*( ( ( ( - 1.0 ) ) ) / stau )) ;
 Dr = Dr  / (1. - dt*( ( ( ( - 1.0 ) ) ) / rtau )) ;
  return 0;
}
 /*END CVODE*/
 static int states () {_reset=0;
 {
   rates ( _threadargscomma_ v ) ;
    s = s + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / stau)))*(- ( ( ( sinf ) ) / stau ) / ( ( ( ( - 1.0 ) ) ) / stau ) - s) ;
    r = r + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / rtau)))*(- ( ( ( rinf ) ) / rtau ) / ( ( ( ( - 1.0 ) ) ) / rtau ) - r) ;
   }
  return 0;
}
 
double alp (  double _lv , double _li ) {
   double _lalp;
 if ( _li  == 0.0 ) {
     _lalp = 7.5 / ( 1.0 + exp ( ( - _lv * 1.0 + 13.0 ) / 7.0 ) ) ;
     }
   else if ( _li  == 1.0 ) {
     _lalp = 0.0068 / ( 1.0 + exp ( ( _lv * 1.0 + 30.0 ) / 12.0 ) ) ;
     }
   
return _lalp;
 }
 
static void _hoc_alp(void) {
  double _r;
    _r =  alp (  *getarg(1) , *getarg(2) );
 hoc_retpushx(_r);
}
 
static double _npy_alp(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r =  alp (  *getarg(1) , *getarg(2) );
 return(_r);
}
 
double bet (  double _lv , double _li ) {
   double _lbet;
 if ( _li  == 0.0 ) {
     _lbet = 1.65 / ( 1.0 + exp ( ( _lv * 1.0 - 14.0 ) / 4.0 ) ) ;
     }
   else if ( _li  == 1.0 ) {
     _lbet = 0.06 / ( 1.0 + exp ( - _lv * 1.0 / 11.0 ) ) ;
     }
   
return _lbet;
 }
 
static void _hoc_bet(void) {
  double _r;
    _r =  bet (  *getarg(1) , *getarg(2) );
 hoc_retpushx(_r);
}
 
static double _npy_bet(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r =  bet (  *getarg(1) , *getarg(2) );
 return(_r);
}
 static double _mfac_rates, _tmin_rates;
 static void _check_rates();
 static void _check_rates() {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  if (!usetable) {return;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_rates =  - 100.0 ;
   _tmax =  100.0 ;
   _dx = (_tmax - _tmin_rates)/200.; _mfac_rates = 1./_dx;
   for (_i=0, _x=_tmin_rates; _i < 201; _x += _dx, _i++) {
    _f_rates(_x);
    _t_sinf[_i] = sinf;
    _t_rinf[_i] = rinf;
    _t_stau[_i] = stau;
    _t_rtau[_i] = rtau;
   }
  }
 }

 static int rates(double _lv){ _check_rates();
 _n_rates(_lv);
 return 0;
 }

 static void _n_rates(double _lv){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 _f_rates(_lv); return; 
}
 _xi = _mfac_rates * (_lv - _tmin_rates);
 if (std::isnan(_xi)) {
  sinf = _xi;
  rinf = _xi;
  stau = _xi;
  rtau = _xi;
  return;
 }
 if (_xi <= 0.) {
 sinf = _t_sinf[0];
 rinf = _t_rinf[0];
 stau = _t_stau[0];
 rtau = _t_rtau[0];
 return; }
 if (_xi >= 200.) {
 sinf = _t_sinf[200];
 rinf = _t_rinf[200];
 stau = _t_stau[200];
 rtau = _t_rtau[200];
 return; }
 _i = (int) _xi;
 _theta = _xi - (double)_i;
 sinf = _t_sinf[_i] + _theta*(_t_sinf[_i+1] - _t_sinf[_i]);
 rinf = _t_rinf[_i] + _theta*(_t_rinf[_i+1] - _t_rinf[_i]);
 stau = _t_stau[_i] + _theta*(_t_stau[_i+1] - _t_stau[_i]);
 rtau = _t_rtau[_i] + _theta*(_t_rtau[_i+1] - _t_rtau[_i]);
 }

 
static int  _f_rates (  double _lv ) {
   double _la , _lb ;
 _la = alp ( _threadargscomma_ _lv , 0.0 ) ;
   _lb = bet ( _threadargscomma_ _lv , 0.0 ) ;
   stau = 1.0 / ( _la + _lb ) ;
   sinf = _la / ( _la + _lb ) ;
   _la = alp ( _threadargscomma_ _lv , 1.0 ) ;
   _lb = bet ( _threadargscomma_ _lv , 1.0 ) ;
   rtau = 1.0 / ( _la + _lb ) ;
   rinf = _la / ( _la + _lb ) ;
    return 0; }
 
static void _hoc_rates(void) {
  double _r;
     _r = 1.;
 rates (  *getarg(1) );
 hoc_retpushx(_r);
}
 
static double _npy_rates(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
  _r = 1.;
 rates (  *getarg(1) );
 return(_r);
}
 
static int _ode_count(int _type){ return 2;}
 
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
     _ode_spec1 ();
  }}
 
static void _ode_map(Prop* _prop, int _ieq, neuron::container::data_handle<double>* _pv, neuron::container::data_handle<double>* _pvdot, double* _atol, int _type) { 
  _ppvar = _nrn_mechanism_access_dparam(_prop);
  _cvode_ieq = _ieq;
  for (int _i=0; _i < 2; ++_i) {
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
 _ode_matsol_instance1(_threadargs_);
 }}

static void initmodel() {
  int _i; double _save;_ninits++;
 _save = t;
 t = 0.0;
{
  r = r0;
  s = s0;
 {
   rates ( _threadargscomma_ v ) ;
   s = sinf ;
   r = rinf ;
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
 initmodel();
 }}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
   ica = gcabar * s * r * ( v - eca ) ;
   }
 _current += ica;

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
 auto const _g_local = _nrn_current(_v + .001);
 	{ double _dica;
  _dica = ica;
 _rhs = _nrn_current(_v);
  _ion_dicadv += (_dica - ica)/.001 ;
 	}
 _g = (_g_local - _rhs)/.001;
  _ion_ica += ica ;
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
 { error =  states();
 if(error){
  std_cerr_stream << "at line 52 in file lcafixed.mod:\nBREAKPOINT {\n";
  std_cerr_stream << _ml << ' ' << _iml << '\n';
  abort_run(error);
}
 } }}

}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = {s_columnindex, 0};  _dlist1[0] = {Ds_columnindex, 0};
 _slist1[1] = {r_columnindex, 0};  _dlist1[1] = {Dr_columnindex, 0};
   _t_sinf = makevector(201*sizeof(double));
   _t_rinf = makevector(201*sizeof(double));
   _t_stau = makevector(201*sizeof(double));
   _t_rtau = makevector(201*sizeof(double));
_first = 0;
}

#if NMODL_TEXT
static void register_nmodl_text_and_filename(int mech_type) {
    const char* nmodl_filename = "/Users/shraddhapathak/Downloads/2487-master/lcafixed.mod";
    const char* nmodl_file_text = 
  "TITLE LCa calcium channel with fixed reversal potential\n"
  ": LCa channel with parameters from US Bhalla and JM Bower,\n"
  ": J. Neurophysiol. 69:1948-1983 (1993)\n"
  ": Adapted from /usr/local/neuron/demo/release/nachan.mod - squid\n"
  ": by Andrew Davison, The Babraham Institute.\n"
  ": 25-08-98\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX lcafixed\n"
  "	USEION ca WRITE ica\n"
  "	RANGE gcabar, ica\n"
  "	GLOBAL sinf, rinf, stau, rtau\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	(mA) = (milliamp)\n"
  "	(mV) = (millivolt)\n"
  "	(molar) = (1/liter)\n"
  "	(mM) = (millimolar)\n"
  "}\n"
  "\n"
  "\n"
  "INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}\n"
  "\n"
  "CONSTANT { eca = 70 (mV) }\n"
  "\n"
  "PARAMETER {\n"
  "	v (mV)\n"
  "	dt (ms)\n"
  "	gcabar	= 0.120 (mho/cm2) <0,1e9>\n"
  ":	eca = 70 (mV)\n"
  "}\n"
  "\n"
  "STATE {\n"
  "	r s\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	ica (mA/cm2)\n"
  "	sinf\n"
  "	rinf\n"
  "	stau (ms)\n"
  "	rtau (ms)\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "	rates(v)\n"
  "	s = sinf\n"
  "	r = rinf\n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "	SOLVE states METHOD cnexp\n"
  "	ica = gcabar*s*r*(v - eca)\n"
  "}\n"
  "\n"
  "DERIVATIVE states {\n"
  "	rates(v)\n"
  "	s' = (sinf - s)/stau\n"
  "	r' = (rinf - r)/rtau\n"
  "}\n"
  "\n"
  "FUNCTION alp(v(mV),i) (/ms) {\n"
  "	if (i==0) {\n"
  "		alp = 7.5(/ms)/(1 + exp((-v *1(/mV) + 13)/7))\n"
  "	}else if (i==1){\n"
  "		alp = 0.0068(/ms)/(1 + exp((v *1(/mV) + 30)/12))\n"
  "	}\n"
  "}\n"
  "\n"
  "FUNCTION bet(v(mV),i)(/ms) {\n"
  "	if (i==0) {\n"
  "		bet = 1.65(/ms)/(1 + exp((v *1(/mV) - 14)/4))\n"
  "	}else if (i==1){\n"
  "		bet = 0.06(/ms)/(1 + exp(-v* 1(/mV)/11))\n"
  "	}\n"
  "}\n"
  "\n"
  "PROCEDURE rates(v(mV)) {LOCAL a, b\n"
  "	TABLE sinf, rinf, stau, rtau FROM -100 TO 100 WITH 200\n"
  "	a = alp(v,0)  b=bet(v,0)\n"
  "	stau = 1/(a + b)\n"
  "	sinf = a/(a + b)\n"
  "	a = alp(v,1)  b=bet(v,1)\n"
  "	rtau = 1/(a + b)\n"
  "	rinf = a/(a + b)\n"
  "}\n"
  "\n"
  ;
    hoc_reg_nmodl_filename(mech_type, nmodl_filename);
    hoc_reg_nmodl_text(mech_type, nmodl_file_text);
}
#endif
