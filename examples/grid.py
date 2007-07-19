#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
""" Expandable example. """


# Standard library imports.
import os, sys

# Major package imports.
import wx

# Put the Enthought library on the Python path.
sys.path.append(os.path.abspath(r'..\..\..'))

# Enthought library imports.
from enthought.pyface.api import GUI, PythonShell, SplitApplicationWindow
from enthought.pyface.grid.api import Grid, TraitGridModel, SimpleGridModel, GridRow, GridColumn, TraitGridColumn
from enthought.traits.api import Float, Str


class MainWindow(SplitApplicationWindow):
    """ The main application window. """

    #### 'SplitApplicationWindow' interface ###################################

    # The ratio of the size of the left/top pane to the right/bottom pane.
    ratio = Float(0.3)

    # The direction in which the window is split.
    direction = Str('vertical')

    data = [['bob', 1, True, Float],
            ['sarah', 45, True, Str],
            ['jonas', -3, False, direction]]

    rows = [GridRow(name='Row 1'),
            GridRow(name='Row 2'),
            GridRow(name='Row 3')]

    cols = [GridColumn(name='Name'),
            GridColumn(name='Index', read_only=True),
            GridColumn(name='Veracity'),
            GridColumn(name='Object')]

    ###########################################################################
    # Protected 'SplitApplicationWindow' interface.
    ###########################################################################

    def _create_lhs(self, parent):
        """ Creates the left hand side or top depending on the split. """

        #self._model = model = SimpleGridModel(data = self.data,
        #                                      rows = self.rows,
        #                                      columns = self.cols)

        self._model = model = TraitGridModel(data = self.cols,
                                             columns=['name',
                                                      TraitGridColumn(name='read_only', label='Read Only')],
                                             row_name_trait='name')

        self._grid = grid = Grid(parent, model = model)


        self._grid.on_trait_change(self._on_grid_anytrait_changed)

        return grid.control

    def _create_rhs(self, parent):
        """ Creates the right hand side or bottom depending on the split. """

        widget = self._grid

        self._python_shell = PythonShell(parent)
        self._python_shell.bind('widget', widget)
        self._python_shell.bind('w', widget)

        return self._python_shell.control

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_content(self, parent):
        """ Create some context for an expandable panel. """

        tree = FileTree(parent, root=os.path.abspath(os.curdir))

        return tree.control

    #### Trait event handlers #################################################

    def _on_grid_anytrait_changed(self, tree, trait_name, old, new):
        """ Called when any trait on the tree has changed. """

        print 'trait', trait_name, 'value', new

        return


# Application entry point.
if __name__ == '__main__':
    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    # Create and open the main window.
    window = MainWindow()
    window.open()

    # Start the GUI event loop.
    gui.start_event_loop()

##### EOF #####################################################################