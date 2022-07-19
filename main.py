from core.bumblebee_wrapper import BumblebeeWrapper

if __name__ == "__main__":
    bee_wrapper = BumblebeeWrapper(
        config_yaml_name="config")
    bee_wrapper.run_bee()
