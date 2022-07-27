                .add_file_with_content_and_commit(file_name='develop_file_name.txt',
                                                  file_content='Develop content\n',
                                                  message='develop commit')
        expected_status_output = """
        diff --git a/develop_file_name.txt b/develop_file_name.txt
        new file mode 100644
        index 0000000..a3bd4e5
        --- /dev/null
        +++ b/develop_file_name.txt
        @@ -0,0 +1 @@
        +Develop content

        """
        assert_command(["diff"], expected_status_output, indent='')
        assert_command(["diff", "develop"], expected_status_output, indent='')
        assert_command(["diff", "refs/heads/develop"], expected_status_output, indent='')