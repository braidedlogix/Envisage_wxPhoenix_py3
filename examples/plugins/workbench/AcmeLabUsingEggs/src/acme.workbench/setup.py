# Major package imports.
from setuptools import setup, find_packages

setup(
    name='acme.workbench',
    version='0.1a1',
    author='Enthought, Inc',
    author_email='info@enthought.com',
    license='BSD',
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    namespace_packages=['acme', 'acme.workbench'],
    entry_points="""
    [envisage.plugins]
    acme_workbench = acme.workbench.acme_workbench_plugin:AcmeWorkbenchPlugin
    """)
