require_relative 'CustomFormatter'

logger = Logger.new($stdout).tap do |log|
  log.progname = 'HeroParser'
end
logger.formatter = proc{|severity, datetime, progname, msg| 
                        CustomFormatter.new.call(severity, datetime, progname, msg)}


csvFilePath = 'C:\\Users\\Harune\\Downloads\\Fantasy War Tactics - Max Stats - Stats (Live).csv'
skillUrlTemplate = "http://fwt.wikia.com/wiki/%{heroName}/Skills"
characterUrlTemplate = "http://fwt.wikia.com/wiki/%{heroName}"
wikiaImageUrlTemplate = "http://fwt.wikia.com/wiki/File:%{image}"



imageUrlMap = {}

