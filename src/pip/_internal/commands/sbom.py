import logging
import os
from optparse import Values
from typing import List
import json 
# import networkx as nx

import pip._vendor.networkx as nx

from pip._internal.cli import cmdoptions
from pip._internal.cli.cmdoptions import make_target_python
from pip._internal.cli.req_command import RequirementCommand, with_cleanup
from pip._internal.cli.status_codes import SUCCESS
from pip._internal.operations.build.build_tracker import get_build_tracker
from pip._internal.req.req_install import check_legacy_setup_py_options
from pip._internal.utils.misc import ensure_dir, normalize_path, write_output
from pip._internal.utils.temp_dir import TempDirectory

logger = logging.getLogger(__name__)


class SbomCommand(RequirementCommand):
    """
    Generate SBOM for Python projects from:

    - PyPI (and other indexes) using requirement specifiers.
    - VCS project urls.
    - Local project directories.
    - Local or remote source archives.

    pip also supports SBOM generation from "requirements files", which provide
    an easy way to specify a whole environment.
    """

    usage = """
      %prog [options] <requirement specifier> [package-index-options] ...
      %prog [options] -r <requirements file> [package-index-options] ...
      %prog [options] <vcs project url> ...
      %prog [options] <local project path> ...
      %prog [options] <archive url/path> ..."""

    def add_options(self) -> None:
        self.cmd_opts.add_option(cmdoptions.constraints())
        self.cmd_opts.add_option(cmdoptions.requirements())
        self.cmd_opts.add_option(cmdoptions.no_deps())
        self.cmd_opts.add_option(cmdoptions.global_options())
        self.cmd_opts.add_option(cmdoptions.no_binary())
        self.cmd_opts.add_option(cmdoptions.only_binary())
        self.cmd_opts.add_option(cmdoptions.prefer_binary())
        self.cmd_opts.add_option(cmdoptions.src())
        self.cmd_opts.add_option(cmdoptions.pre())
        self.cmd_opts.add_option(cmdoptions.require_hashes())
        self.cmd_opts.add_option(cmdoptions.progress_bar())
        self.cmd_opts.add_option(cmdoptions.no_build_isolation())
        self.cmd_opts.add_option(cmdoptions.use_pep517())
        self.cmd_opts.add_option(cmdoptions.no_use_pep517())
        self.cmd_opts.add_option(cmdoptions.check_build_deps())
        self.cmd_opts.add_option(cmdoptions.ignore_requires_python())

        self.cmd_opts.add_option(
            "-d",
            "--dest",
            "--destination-dir",
            "--destination-directory",
            dest="download_dir",
            metavar="dir",
            default=os.curdir,
            help="Download packages into <dir>.",
        )

        cmdoptions.add_target_python_options(self.cmd_opts)

        index_opts = cmdoptions.make_option_group(
            cmdoptions.index_group,
            self.parser,
        )

        self.parser.insert_option_group(0, index_opts)
        self.parser.insert_option_group(0, self.cmd_opts)

    @with_cleanup
    def run(self, options: Values, args: List[str]) -> int:
        options.ignore_installed = True
        # editable doesn't really make sense for `pip download`, but the bowels
        # of the RequirementSet code require that property.
        options.editables = []

        cmdoptions.check_dist_restriction(options)

        options.download_dir = normalize_path(options.download_dir)
        ensure_dir(options.download_dir)

        session = self.get_default_session(options)

        target_python = make_target_python(options)
        finder = self._build_package_finder(
            options=options,
            session=session,
            target_python=target_python,
            ignore_requires_python=options.ignore_requires_python,
        )

        build_tracker = self.enter_context(get_build_tracker())

        directory = TempDirectory(
            delete=not options.no_clean,
            kind="download",
            globally_managed=True,
        )

        reqs = self.get_requirements(args, options, finder, session)
        check_legacy_setup_py_options(options, reqs)

        preparer = self.make_requirement_preparer(
            temp_build_dir=directory,
            options=options,
            build_tracker=build_tracker,
            session=session,
            finder=finder,
            download_dir=options.download_dir,
            use_user_site=False,
            verbosity=self.verbosity,
        )

        resolver = self.make_resolver(
            preparer=preparer,
            finder=finder,
            options=options,
            ignore_requires_python=options.ignore_requires_python,
            use_pep517=options.use_pep517,
            py_version_info=options.python_version,
        )

        self.trace_basic_info(finder)

        requirement_set = resolver.resolve(reqs, check_supported_wheels=True)

        dependency_graph = nx.DiGraph()

        from pprint import pprint

        pprint(requirement_set.__dict__)

        for req in requirement_set.requirements.values():

            package_name = f"{req.name} {req.metadata.get('Version', '')}"
            dependency_graph.add_node(package_name)
            if req.comes_from:
                try:
                    dependency_graph.add_edge(package_name, f"{req.comes_from.name} {req.comes_from.metadata.get('Version', '')}")
                except AssertionError:
                    continue

        self.generate_cyclonedx_sbom(dependency_graph, options.download_dir, args[1])
        return SUCCESS





    def generate_cyclonedx_sbom(self, graph: nx.DiGraph, output_dir: str, package_name: str) -> None:

        from pip._vendor.cyclonedx.model.bom import Bom
        from pip._vendor.cyclonedx.model.component import Component, ComponentType
        from pip._vendor.cyclonedx.output import BaseOutput
        from pip._vendor.cyclonedx.schema import SchemaVersion, OutputFormat
        from pip._vendor.cyclonedx.output.json import JsonV1Dot5
        import pip._vendor.packageurl as packageurl

        bom = Bom()
        print(graph.nodes)
        
        bom.metadata.component = root_component = Component(
                name=[x.split(" ")[0] for x in graph.nodes if x.split(" ")[0] == package_name][0],
                type=ComponentType.APPLICATION
            ) # type: ignore
        
        # Dictionary to store created components
        created_components = {[x for x in graph.nodes if x.split(" ")[0] == package_name][0]: root_component}

        for node in graph.nodes:
            if node not in created_components:
                name_parts = node.split(" ")
                component_name = name_parts[0]
                component_version = name_parts[1] if len(name_parts) > 1 else None
                purl = packageurl.PackageURL(type="pypi", name=component_name, version=component_version)
                component = Component(type=ComponentType.LIBRARY, name=component_name, version=component_version, purl=purl)
                bom.components.add(component)
                bom.register_dependency(root_component, [component])
                created_components[node] = component
            
            dependencies = list(graph.successors(node))
            if dependencies:
                for dep in dependencies:
                    dep_name_parts = dep.split(" ")
                    dep_component_name = dep_name_parts[0]
                    dep_component_version = dep_name_parts[1] if len(dep_name_parts) > 1 else None

                    if dep not in created_components:
                        dep_component = Component(name=dep_component_name, version=dep_component_version, type=ComponentType.LIBRARY, purl=f"pkg:pypi/{dep_component_name}@{dep_component_version}")
                        created_components[dep] = dep_component
                        bom.components.add(dep_component)
                    bom.register_dependency(created_components[dep], [created_components[node]])


        my_json_outputter = JsonV1Dot5(bom)
        serialized_json = my_json_outputter.output_as_string(indent=2)
        sbom_path = os.path.join(output_dir, "sbom.json")
        
        with open(sbom_path, "w") as sbom_file:
            sbom_file.write(serialized_json)

        print(f"CycloneDX SBOM written to {sbom_path}")

