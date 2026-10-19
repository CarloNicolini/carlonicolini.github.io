# Preserve old inbound URLs while keeping one source asset tree.
module Jekyll
  class LegacyAsset < StaticFile
    def destination(dest)
      File.join(dest, 'static', @dir.delete_prefix('/assets/media'), @name)
    end
    def url
      super.sub(%r{\A/assets/media/}, '/static/')
    end
  end
  class LegacyUrls < Generator
    priority :low
    def generate(site)
      media = site.static_files.select { |file| file.relative_path.start_with?('/assets/media/') }
      media.each do |file|
        relative = file.relative_path
        site.static_files << LegacyAsset.new(site, site.source, File.dirname(relative), File.basename(relative))
      end
      { '/sections/science/' => '/writing/?topic=science', '/sections/tech/' => '/writing/?topic=tech',
        '/sections/finance/' => '/writing/?topic=finance', '/sections/publications/' => '/publications/',
        '/sections/software/' => '/software/', '/sections/cv/' => '/curriculum/',
        '/sections/cv/cv.html' => '/curriculum/', '/sections/publications.html' => '/publications/',
        '/sections/software.html' => '/software/', '/sections/contact.html' => '/curriculum/',
        '/sections/downloads.html' => '/software/', '/blog/' => '/writing/', '/search/' => '/writing/' }.each do |path, target|
        filename = path.end_with?('/') ? 'index.html' : File.basename(path)
        directory = path.end_with?('/') ? path : File.dirname(path)
        page = PageWithoutAFile.new(site, site.source, directory, filename)
        destination = site.baseurl + target
        page.content = "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta http-equiv=\"refresh\" content=\"0;url=#{destination}\"><link rel=\"canonical\" href=\"#{destination}\"><title>Page moved</title></head><body><a href=\"#{destination}\">Continue to the new page</a></body></html>"
        page.data['layout'] = nil
        page.data['sitemap'] = false
        site.pages << page
      end
    end
  end
end
