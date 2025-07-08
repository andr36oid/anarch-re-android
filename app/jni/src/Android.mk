LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := main

$(shell (cd $(LOCAL_PATH)/anarch-re && make assets > /dev/null 2>&1))

# Add your application source files here...
LOCAL_SRC_FILES := \
    anarch-re/main_sdl3.c

SDL_PATH := ../SDL  # SDL

include $(LOCAL_PATH)/anarch-re/config.mk

LOCAL_CFLAGS += -DSFG_VERSION_STRING=\"$(FULL_VERSION)\" \
    -DSFG_IDENTIFIER_STRING=\"$(APP_ID)\"

LOCAL_C_INCLUDES := $(LOCAL_PATH)/$(SDL_PATH)/include  # SDL

LOCAL_SHARED_LIBRARIES := SDL3

LOCAL_LDLIBS := -lGLESv1_CM -lGLESv2 -lOpenSLES -llog -landroid  # SDL

include $(BUILD_SHARED_LIBRARY)
