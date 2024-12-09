from city_scrapers_core.constants import CITY_COUNCIL, COMMITTEE
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import LegistarSpider


class CinohCityCouncilSpider(LegistarSpider):
    name = "cinoh_city_council"
    agency = "Cincinnati City Council"
    timezone = "America/Chicago"
    start_urls = ["https://cincinnatioh.legistar.com/Calendar.aspx"]
    # Add the titles of any links not included in the scraped results
    link_types = []

    def parse_legistar(self, response):
        """
        Oftentimes, the columns: meeting details, agenda, minutes, and video are left blank on the calander
        but when they are, they are in the form of links. 
        """
        for obj in response:
            meeting = Meeting(
                title=obj["Name"]["label"],
                description="",
                classification=self._parse_classification(obj),
                start=self.legistar_start(obj),
                end=None,
                all_day=False,
                time_notes="",
                location=self._parse_location(obj),
                links=self._parse_links(obj),
                source=self.legistar_source(obj),
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_classification(self, obj):
        if obj["Name"]["label"] == "Cincinnati City Council":
            return CITY_COUNCIL
        else:
            return COMMITTEE

    def _parse_location(self, obj):
        room = obj["Meeting Location"]
        return {
            "address": "801 Plum St. Cincinnati, OH 45202",
            "name": f"{room}"
        }
    
    def _parse_links(self, obj):
        links = []
        if obj.get("Name"):
            links.append({"title": "meeting page", "href": obj["Name"]["url"]})
        if obj.get("iCalendar"):
            links.append({"title": "iCalendar", "href": obj["iCalendar"]["url"]})
        if obj.get("Meeting Details"):
            links.append({"title": "Meeting Details", "href": obj["Meeting Details"]["url"]})
        if obj.get("Agenda"):
            links.append({"title": "Agenda", "href": obj["Agenda"]["url"]})
        if obj.get("Agenda Packet"):
            links.append({"title": "Agenda Packet", "href": obj["Agenda Packet"]["url"]})
        if obj.get("Minutes"):
            links.append({"title": "Minutes", "href": obj["Minutes"]["url"]})
        if obj.get("Video"):
            links.append({"title": "Video", "href": obj["Video"]["url"]})
        return links

