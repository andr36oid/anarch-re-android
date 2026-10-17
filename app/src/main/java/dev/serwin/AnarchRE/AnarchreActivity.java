package dev.serwin.AnarchRE;

import android.view.InputDevice;

import org.libsdl.app.SDLActivity;

public class AnarchreActivity extends SDLActivity
{
    /**
     * No touch controls on devices without a touchscreen, like handhelds with buttons:
     * they would cover the game and only go away on a keyboard key, not a gamepad button.
     */
    @Override
    protected String[] getArguments() {
        for (int id : InputDevice.getDeviceIds()) {
            InputDevice device = InputDevice.getDevice(id);
            if (device != null && device.supportsSource(InputDevice.SOURCE_TOUCHSCREEN)) {
                return new String[0];
            }
        }
        return new String[] { "--touch", "never" };
    }
}
