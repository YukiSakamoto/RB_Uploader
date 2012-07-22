#!/usr/bin/ruby -Ku
#!/usr/local/bin/ruby -Ku

require 'erb'
require "yaml/store"
require "cgi"
#Test Under Ruby 1.8.7
#========================================
#	Environment Definitions
#========================================
load "./uploader_settings.rb"
include Settings
STATUS = 'status'	#<- Do Not Change

cgi = CGI.new
#category.class => Fixnum
if cgi.params['category'] == nil
	category = 0
	filter = false
elsif (category = cgi.params['category'][0]) == nil
	category = 0
	filter = false
elsif (category = category.to_i) == 0
	filter = false
else
	filter = true
end

current_category_name = String.new
if category == 0
	current_category_name = "All"
else
	current_category_name = CategoryName[category-1].to_s
end

db = YAML::Store.new(LogFile)
counter = 0
total_size = 0					#export for html file
table_main = String.new				#export for html file
category_list_tag = String.new
db.transaction do
	if db["status"]
		counter = db["status"]["count"]
	else 
		db["status"] = Hash.new
		db["status"]["count"] = 0
	end
end

registration_category = String.new
tempstr = String.new
CategoryName.each_with_index do |cate, index|
	tempstr = <<HERE
	<option value="#{index+1}">#{cate}</option>
HERE
registration_category += tempstr
end

view_category = <<HERE
	<option value="0">All View</option>
HERE
view_category += registration_category

#making table
counter.downto(1) do |i|
	registration = nil
	db.transaction do
		registration = db[i]
	end

	if registration == nil || registration['existence'] == false
		next
	elsif filter == true && registration['category'] != category
		next
	end

	total_size += (registration['filesize'] || 0 )
	filename = registration['registration_filename']
	temp = String.new
	temp = <<HERE

				<tr class="resources">
					<td class="number"> #{i} </td>
					<td class="name"> #{registration['name']} </td>
					<td class="date"> #{registration['date']} </td>
					<td class="filaname"> <a href="#{Storage_Dir + "/" + filename}">#{filename} </a></td>
					<td class="comment"> #{registration['comment']} </td>
					<td class="filesize"> #{registration['filesize']/1024 || 0.0} </td>
					<!-- #{registration['src_filename']} -->
				</tr>
HERE
table_main += temp
end

print "Content-type: text/html\n\n"
puts ERB.new(File.read('./listpage2.html')).result(binding)
