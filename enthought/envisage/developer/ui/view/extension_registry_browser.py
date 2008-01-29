""" A view showing a summary of the running application. """


# Standard library imports.
import inspect

# Enthought library imports.
from enthought.envisage.api import IApplication, IExtensionPoint
from enthought.envisage.api import IExtensionRegistry, Service
from enthought.envisage.developer.code_browser.api import CodeBrowser
from enthought.io.api import File
from enthought.traits.api import Any, HasTraits, Instance
from enthought.traits.ui.api import Item, View

# fixme: non-api import.
from enthought.plugins.text_editor.editor.text_editor import TextEditor

# Local imports.
from extension_registry_browser_tree_editor import \
     extension_registry_browser_tree_editor


extension_registry_browser_view = View(
    Item(
        name       = 'application',
        show_label = False,
        editor     = extension_registry_browser_tree_editor
    ),

    resizable = True,
    style     = 'custom',
    title     = 'Extension Registry',

    width     = .2,
    height    = .4
)


class ExtensionRegistryBrowser(HasTraits):
    """ An extension registry browser.

    Actually, this class exists just because to use a trait editor we have
    to have a trait to edit!

    """

    #### 'ExtensionRegistryBrowser' interface #################################

    # The application that whose extension registry we are browsing.
    application = Instance(IApplication)

    # The code browser that we use to parse plugin source code.
    code_browser = Instance(CodeBrowser)
    
    # The workbench service.
    workbench = Service('enthought.envisage.ui.workbench.api.Workbench')
    
    # The default traits UI view.
    traits_view = extension_registry_browser_view

    ###########################################################################
    # 'ExtensionRegistryBrowser' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _extension_registry_default(self):
        """ Trait initializer. """

        return self.application.extension_registry
    
    #### Methods ##############################################################
    
    def dclick(self, obj):
        """ Called when an object in the tree is double-clicked. """

        if IExtensionPoint(obj, None) is not None:
            # Find the plugin that offered the extension point.
            plugin = self._get_plugin(obj)

            # Parse the plugin source code.
            module = self._parse_plugin(plugin)

            # Get the plugin klass.
            klass = self._get_plugin_klass(module, plugin)
            
            # Edit the plugin.
            editor = self.workbench.edit(
                self._get_file_object(plugin), kind=TextEditor
            )
            
            # Was the extension point offered declaratively via a trait?
            trait_name = self._get_extension_point_trait(plugin, obj.id)
            if trait_name is not None:
                attribute = klass.attributes.get(trait_name)
                lineno    = attribute.lineno

            else:
                lineno = klass.lineno

            editor.center_line(lineno-1)
            editor.select_line(lineno-1)

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_extension_point_trait(self, plugin, id):
        """ Return the extension point trait with the specifed Id.

        Return None if the extension point was not declared via a trait.

        """

        for name, trait in plugin.traits(__extension_point__=True).items():
            if trait.trait_type.id == id:
                break

            else:
                name = None

        return name
        
    def _get_plugin(self, extension_point):
        """ Return the plugin that offered an extension point. """

        for plugin in self.application:
            if extension_point in plugin.get_extension_points():
                break

        else:
            plugin = None

        return plugin

    def _get_plugin_klass(self, module, plugin):
        """ Get the klass that defines the plugin. """
        
        for name, klass in module.klasses.items():
            if name == type(plugin).__name__:
                break

        else:
            klass = None
            
        return klass
    
    def _get_file_object(self, obj):
        """ Return a 'File' object for the object's source file. """
        
        return File(path=inspect.getsourcefile(type(obj)))

    def _parse_plugin(self, plugin):
        """ Parse the plugin source code. """

        filename = self._get_file_object(plugin).path

        return self.code_browser.read_file(filename)
    
#### EOF ######################################################################
