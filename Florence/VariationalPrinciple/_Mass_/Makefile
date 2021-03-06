PYTHON_VERSION = python2.7
PYTHON_LANG_LEVEL = 2
PYTHON_INCLUDE_PATH = /usr/include/python2.7/
PYTHON_LD_PATH = /usr/lib/
EXT_POSTFIX= so
CYTHONFLAGS = -DNPY_NO_DEPRECATED_API

CYTHON = cython --cplus -$(PYTHON_LANG_LEVEL)

ifeq ($(OS),Windows_NT)
REMOVE = del
MOVE = move
else
REMOVE = rm -rf
MOVE = mv
endif

ADDITIONAL_FLAGS =

INLINE_THRESHOLD = 100000
CXXSTD=-std=c++11
OPTFLAGS= -O3 -fno-strict-aliasing -DNDEBUG
CXXFLAGS= -fPIC -shared -pthread -Wall $(CYTHONFLAGS) $(OPTFLAGS)

BLAS_VERSION = openblas
BLAS_INCLUDE_PATH = /opt/OpenBLAS/include/
BLAS_LD_PATH = /opt/OpenBLAS/lib/

ifeq ($(findstring mkl,$(BLAS_VERSION)),mkl)
CXXFLAGS += -DHAS_MKL
endif

NUMPY_INCLUDE_PATH = /usr/local/lib/python2.7/dist-packages/numpy/core/include

ifeq ($(findstring g++,$(CXX)),g++)
ifneq ($(findstring clang++,$(CXX)),clang++)
CXXFLAGS += -Wno-cpp -Wno-unused-function -Wno-maybe-uninitialized -fabi-version=6
CXXFLAGS += -march=native -ffast-math -fwrapv -funroll-loops -finline-functions -finline-limit=$(INLINE_THRESHOLD) -ffp-contract=fast
else
CXXFLAGS += -Wno-uninitialized -Wno-missing-braces -Wno-#warnings
CXXFLAGS += -march=native -ffast-math -mllvm -inline-threshold=$(INLINE_THRESHOLD) -ffp-contract=fast
endif
endif
ifeq ($(findstring c++,$(CXX)),c++)
CXXFLAGS += -Wno-uninitialized -Wno-missing-braces -Wno-#NPY_NO_DEPRECATED_API
CXXFLAGS += -march=native -ffast-math -mllvm -inline-threshold=$(INLINE_THRESHOLD) -ffp-contract=fast
endif
ifeq ($(findstring icpc,$(CXX)),icpc)
CXXFLAGS += -march=native -no-ansi-alias -xHost -fp-model fast=1 -inline-forceinline -inline-factor=$(INLINE_THRESHOLD)
endif

# On some architectures -march=native does not define -mfma
HAS_FMA := $(shell $(CXX) -march=native -dM -E - < /dev/null | egrep "AVX2" | sort)
ifeq ($(HAS_FMA),)
else
CXXFLAGS += -mfma
endif

ifeq ($(OS),Windows_NT)
CXXFLAGS += -D_hypot=hypot -m64 -Wno-format-extra-args -Wno-format
endif

FASTOR_OPTFLAGS = -DFASTOR_NO_ALIAS -DFASTOR_USE_VECTORISED_EXPR_ASSIGN -DCONTRACT_OPT=2 -DFASTOR_NO_STATIC_WARNING
CXXFLAGS += $(FASTOR_OPTFLAGS) -I$(FASTOR_INCLUDE_PATH)

CXXFLAGS += $(ADDITIONAL_FLAGS)

all: build_module

build_module:
	@echo "Building low level mass dispatcher module"
	$(CYTHON) _MassIntegrand_.pyx
	$(CXX) $(CXXSTD) $(CXXFLAGS) _MassIntegrand_.cpp -o _MassIntegrand_.$(EXT_POSTFIX) -I. -I../../Tensor/ -I$(PYTHON_INCLUDE_PATH) \
	-I$(NUMPY_INCLUDE_PATH) -I$(BLAS_INCLUDE_PATH) -L$(PYTHON_LD_PATH) -l$(PYTHON_VERSION) -L$(BLAS_LD_PATH) -l$(BLAS_VERSION) \
	-I../../FiniteElements/Assembly/_Assembly_/
	@$(MOVE) _MassIntegrand_.$(EXT_POSTFIX) ../

clean:
	$(REMOVE) _MassIntegrand_.cpp _MassIntegrand_.$(EXT_POSTFIX) ../_MassIntegrand_.$(EXT_POSTFIX)

source_clean:
	$(REMOVE) _MassIntegrand_.cpp