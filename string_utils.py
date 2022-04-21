from amf_handler import amf_handler
import traceback

class string_utils(amf_handler):
    def run(self):
        self.set_logger(__name__)
        try:
            self.get_config()
            result = self.process()
            self.generate_output(result)
            self.set_status('ok', '')
        except:
            self.set_status("Failed", traceback.format_exc())

    def get_config(self):
        self.data = self.read_input_data_string()
        self.msg = self.get_message_properties()
        self.parms = self.get_action_parameters()

    def process(self):
        if self.parms['action'] == 'TO_UPPER':
            newdata = self.data.upper()
        elif self.parms['action'] == 'TO_LOWER':
            newdata = self.data.lower()
        elif self.parms['action'] == 'REPLACE_STR':
            findstr = self.parms['STRING_TO_FIND']
            replacestr = self.parms['STRING_TO_REPLACE']
            newdata = self.data.replace(bytes(findstr,'utf-8'),bytes(replacestr,'utf-8'))
        return newdata

    def generate_output(self, outdata):
        prefix = 'processed_'
        if 'PREFIX' in self.parms:
            prefix = self.parms['PREFIX']
        self.msg.file_name = prefix+self.msg.file_name
        handle = self.get_output_data_handle()
        handle.write(outdata)
        handle.close()
        self.register_output_message(self.msg)
        self.log_event('Info','Output generated successfully as '+self.msg.file_name)
        self.log_event('Info','Wrote {} bytes'.format(len(outdata)))


