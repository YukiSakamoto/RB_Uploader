#!/usr/bin/ruby -Ku
#!/usr/local/bin/ruby -Ku
require "cgi"
require "yaml/store"

#Test: Under Ruby 1.8.7
#========================================
#	Environment Definitions
#========================================
load "uploader_settings.rb"
include Settings
STATUS		 = "status"	#Do Not Change
#========================================
#	KEYWORD Definitions
#========================================
#===========FieldName====================
Operation_Code  = 'ope_code'
Contributor_Name= 'name'
UploadFile      = 'upload_file'
Comment         = 'comment'
Change_Number   = 'number'
Password        = 'passcode'
Category 	= 'category'
#===========Operation Code ==============
Ope_FileUpload    = "file_upload"
Ope_FileRemove    = "file_remove"
Ope_ChangeComment = "change_comment"


include Settings
#========================================
#	Utility Function Definitions
#========================================
def get_newfilename(count, extension)
	return "#{UploaderName}#{count}#{extension}"
end

def make_TimeString
	time = Time.now
	buf = String.new
	week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
	return sprintf("%4d/%02d/%02d(%s) %02d:%02d", time.year, time.month, time.day, week[time.wday], time.hour, time.min)
end

def build_temppage(type, retcode, other_msg = nil)
	redirect_time = 1	#seconds
	print "Content-type: text/html\n\n"
	print "<html>\n"
	print "<head>\n"
	print "<META HTTP-EQUIV=\"Refresh\" CONTENT=\"#{redirect_time}; URL=#{RedirectDestination} \">\n"
	print "</head>\n"
	print "<body>\n"

	if retcode == true
		print "<p>#{type} Success<br> \n</p>"
	elsif retcode == false
		print "<p>#{type} Failure<br> \n</p>"
	elsif retcode == nil
		;
	end

	print "<p>#{other_msg}<\p>"	if other_msg
	print "<p> Please wait for a few seconds...</p>"
	print "</body>\n"
	print "</html>\n"
end

#========================================
#	Operation Functions
#========================================
def upload_main(cgi)
	name = CGI.escapeHTML(cgi.params[Contributor_Name][0].read)
	comment = CGI.escapeHTML(cgi.params[Comment][0].read)
	upload_file_IO = cgi.params[UploadFile][0]
	src_filename = CGI.escapeHTML(upload_file_IO.original_filename)
	filesize = upload_file_IO.size
	date = make_TimeString()
	extension = File.extname(src_filename)

	category = cgi.params[Category][0].read.to_i

	#Form Data Checking
	if (name == nil || name.length == 0 ||
		comment == nil || comment.length == 0 || 
		src_filename == nil || src_filename.length == 0 )
		return build_temppage("Uploading", false, nil)
	end

	if LimitFileSize && LimitFileSize < filesize
		return build_temppage("Uploading", false, "Too Large File!!")
	end

	# Extension Check
	Restrict_Ext.each do |ext|
		if ext[0..0] != "." 
			ext = "." + ext
		end
		if ext == extension
			return build_temppage("Uploading", false, "Invalid Extensions")
		end
	end

	#DataBase Open...
	db = YAML::Store.new(LogFile)

	#count increment.
	count = 0
	status = Hash.new
	db.transaction do
		status = db[STATUS]
	end
	if status && count = status["count"]
		count += 1
	else
		status = Hash.new
		count = 1
	end
	status["count"] = count
	#Making Registration Data
	filename = get_newfilename(count, extension)

	
	registration_data = {'name' => name, 'comment' => comment, 'registration_filename' => filename,
				'src_filename' => src_filename, 'date' => date, 'existence' => true,
				'filesize' => filesize,	'category' => category			}

	#Exec Registration
	db.transaction do
		db[count] = registration_data
		db[STATUS] = status
	end

	#File Copy
	File.open(Storage_Dir + '/' + filename, "w") do |file|
		file.binmode
		file.write(upload_file_IO.read)
	end

	return build_temppage("Upload", true)
end

def file_remove(cgi)
	number = cgi.params[Change_Number][0].read.to_i
	filename = String.new
	del_data = nil

	db = YAML::Store.new(LogFile)
	#Registration Check
	db.transaction do
		del_data = db[number]	
	end

	if del_data == nil || del_data['existence'] == false
		return build_temppage("File Remove", false, "No Existence")
	end

	filename = del_data['registration_filename']

	#Registration Edit
	db.transaction do
		db[number]['existence'] = false
	end

	#Throwing Success Code, Here.
	build_temppage("Delete", true)

	File.delete(Storage_Dir + '/' + filename)
end

def change_comment(cgi)
	number	= cgi.params[Change_Number][0].read.to_i
	comment = CGI.escapeHTML(cgi.params[Comment][0].read)

	data = nil
	db = YAML::Store.new(LogFile)
	db.transaction do
		data = db[number]
	end
	#Registration Check
	if data ==nil || data['existence'] == false
		return build_temppage("Chaging Comment", false, "File Does Not Exist!")
	end

	#Changing Registration
	db.transaction do
		db[number]['comment'] = comment
	end
	build_temppage("Changing Comment", true)
end

#========================================
#	Main (Entry Point).
#========================================
if __FILE__ == $0	#Main Routine 
	begin
		cgi = CGI.new
		ope_code = cgi.params[Operation_Code][0].read
		if ope_code == Ope_FileUpload
			upload_main(cgi)
		elsif ope_code == Ope_FileRemove
			file_remove(cgi)
		elsif ope_code == Ope_ChangeComment
			change_comment(cgi)
		else
			build_temppage("Operation", false, 
				       "Operation Code: #{ope_code} is wring. <br>Please tell this Bug to the Administrator.")
		end
	rescue => exception
		build_temppage("Operation", false, "Uploader Error!")
		#build_temppage(exception, false, "Uploader_Error")
	end
end	#Main Routine End

