class TestRegisterChannel:
    def test_should_register_channel(self):
        channel_data = {
            "chat_identifier": "https://t.me/phprio/165249",
            "api_key": "0000000000",
            "channel_name": "PHP Rio Vagas",
            "tags": ["CSS", "PHP", "PostgreSQL"]
        }

        channel_repository:ChannelRepositoryMem


