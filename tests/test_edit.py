
from pytest_mock import MockerFixture

from .base_test import BaseTest
from .mockers import (assert_failure, assert_success, launch_command,
                      overridden_environment)

dummy_editor = "sh -c 'echo foo > $1' 'ignored_$0'"


class TestEdit(BaseTest):

    def test_edit_git_machete_editor(self) -> None:
        with overridden_environment(GIT_MACHETE_EDITOR=dummy_editor):
            launch_command("edit")
        assert self.repo_sandbox.read_file(".git/machete").strip() == "foo"

    def test_edit_git_machete_editor_not_valid_executable(self, mocker: MockerFixture) -> None:
        with overridden_environment(GIT_MACHETE_EDITOR="lolxd-this-doesnt-exist"):
            assert_failure(["edit"], "'$GIT_MACHETE_EDITOR' (lolxd-this-doesnt-exist) is not available")

    def test_edit_git_editor(self) -> None:
        self.repo_sandbox.set_git_config_key("advice.macheteEditorSelection", "true")

        with overridden_environment(GIT_EDITOR=dummy_editor):
            assert_success(
                ["edit"],
                """
                Opening '$GIT_EDITOR' (sh -c 'echo foo > $1' 'ignored_$0').
                To override this choice, use GIT_MACHETE_EDITOR env var, e.g. export GIT_MACHETE_EDITOR=vi.

                See git machete help edit and git machete edit --debug for more details.

                Use git config --global advice.macheteEditorSelection false to suppress this message.
                """
            )
        assert self.repo_sandbox.read_file(".git/machete").strip() == "foo"

    def test_edit_git_config_core_editor(self) -> None:
        self.repo_sandbox.set_git_config_key("advice.macheteEditorSelection", "false")

        with overridden_environment(GIT_MACHETE_EDITOR="  ", GIT_EDITOR="lolxd-this-doesnt-exist", VISUAL="", EDITOR=dummy_editor):
            assert_success(["edit"], "")
        assert self.repo_sandbox.read_file(".git/machete").strip() == "foo"

    def test_edit_no_variant_matches(self, mocker: MockerFixture) -> None:
        self.patch_symbol(mocker, "git_machete.utils.find_executable", lambda executable: None)

        with overridden_environment(GIT_MACHETE_EDITOR="  ", GIT_EDITOR="lolxd-this-doesnt-exist", VISUAL="", EDITOR=""):
            assert_failure(
                ["edit"],
                "Cannot determine editor. Set GIT_MACHETE_EDITOR environment variable or edit .git/machete directly."
            )
