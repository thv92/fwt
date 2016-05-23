require 'logger'
class CustomFormatter < Logger::Formatter
    def call(severity, datetime, progname, msg)
        # msg2str is the internal helper that handles different msgs correctly
        "#{severity} [#{datetime.strftime("%d-%b-%Y %H:%M:%S.%L")} #{progname}]: #{msg2str(msg)}"
    end
end