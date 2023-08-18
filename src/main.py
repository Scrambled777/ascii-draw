# main.py
#
# Copyright 2023 Nokse
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw, Gdk
from .window import AsciiDrawWindow


class AsciiDrawApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='io.github.nokse22.asciidraw',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)

        css = '''
        .ascii-textview{
            /*background-image:  linear-gradient(#f6f5f4 1px, transparent 1px), linear-gradient(to right, #f6f5f4 1px, #f6f5f4 1px);
            */
            background-color: #f6f5f4;
            background:
                linear-gradient(-90deg, rgba(0,0,0,.05) 1px, transparent 1px),
                linear-gradient(rgba(0,0,0,.05) 1px, transparent 1px),
                linear-gradient(-90deg, rgba(0, 0, 0, .04) 1px, transparent 1px),
                linear-gradient(rgba(0,0,0,.04) 1px, transparent 1px),
                linear-gradient(transparent 3px, #f6f5f4 3px, #f6f5f4 78px, transparent 78px),
                linear-gradient(-90deg, #aaa 1px, transparent 1px),
                linear-gradient(-90deg, transparent 3px, #f6f5f4 3px, #f6f5f4 78px, transparent 78px),
                linear-gradient(#aaa 1px, transparent 1px),
                #f6f5f4;
            background-size:
                12px 24px,
                12px 24px,
                60px 72px,
                60px 72px,
                60px 72px,
                60px 72px,
                60px 72px,
                60px 72px;
            box-shadow: 0px 0px 10px 10px #c0bfbc44;
        }
        .ascii-preview{
            background: transparent;
            opacity: 0.3;
            background-size: 12px 24px;
        }
        .ascii{
            font-family: Monospace;
            font-size: 20px;
            color:black;
        }
        .mono-entry{
            font-family: Monospace;
            font-size: 20px;
            padding: 0px;
            border-radius: 0px;
            border: 1px solid black;
        }
        .split-button{
            padding: 0px;
        }
        '''
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css, -1)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = AsciiDrawWindow(application=self)
        win.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='ascii-draw',
                                application_icon='io.github.nokse22.asciidraw',
                                developer_name='Nokse',
                                version='0.1.0',
                                developers=['Nokse'],
                                copyright='© 2023 Nokse')
        about.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('app.preferences action activated')

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = AsciiDrawApplication()
    return app.run(sys.argv)