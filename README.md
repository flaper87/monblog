MonBlog
=======

GridFS based blog engine.

Getting Started
===============


### Posts

Posts are plain text files that can be written down using markdown (Hopefully it'll support more syntaxes). Each post can contain a json serialized metadata object that can be used to define custom fields and properties for each post.  

	$"metadata"$
	{ "title": "test", "md": true, "tags": ["test"]}
	$"metadata"$
	
	
	**THE MOST AMAZING BLOG POST**


### Upload

Posts have to be "uploaded" to the blog engine using the `upload` command.

	monblog upload -f my_new_blog_post


It is possible to upload posts to a remote server using the `dbhost` param.


	monblog upload --dbhost blog.monblog.com -f my_new_blog_post


### Export

It is possible to export posts using the `export` command. (Posts will be exported using the same format)

	monblog export -d exported_posts/ -n 10


TODO
====

* Write more docs

* Improve Metada Syntax

* Add git / HG post "push" hooks in order to manage "publish" actions with a normal git repository.


LICENSE
=======

This software is licensed under the New BSD License. See the LICENSE file in the top distribution directory for the full license text.
