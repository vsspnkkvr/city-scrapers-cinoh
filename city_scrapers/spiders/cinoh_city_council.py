from city_scrapers_core.constants import CITY_COUNCIL, COMMITTEE
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import LegistarSpider


class CinohCityCouncilSpider(LegistarSpider):
    name = "cinoh_city_council"
    agency = "Cincinnati City Council"
    timezone = "America/New_York"
    start_urls = ["https://cincinnatioh.legistar.com/Calendar.aspx"]

    def parse_legistar(self, response):
        """
        Parse upcoming and past meetings from the Cincinnati City Council meetings table.

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
                status=self._parse_status(obj),
                location=self._parse_location(obj),
                links=self._parse_links(obj),
                source=self.legistar_source(obj),
            )

            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_classification(self, obj):
        if obj["Name"]["label"] == "Cincinnati City Council":
            return CITY_COUNCIL
        else:
            return COMMITTEE
    
    def _parse_status(self, obj):
        if obj["Meeting Location"] == "Council Chambers, Room 300 NOTICE OF CANCELLATION":
            return "cancelled"
        else:
            return "tentative"

    def _parse_location(self, obj):
        room = obj["Meeting Location"]
        return {
            "address": "801 Plum St. Cincinnati, OH 45202",
            "name": f"{room}"
        }
    
    def _parse_links(self, obj):
        
        if obj.get("Name"):
            return [{"title": "meeting page", "href": obj["Name"]["url"]}]
        if obj.get("iCalendar"):
            return [{"title": "iCalendar", "href": obj["iCalendar"]["url"]}]
        if obj.get("Meeting Details"):
            return [{"title": "Meeting Details", "href": obj["Meeting Details"]["url"]}]
        if obj.get("Agenda"):
            return [{"title": "Agenda", "href": obj["Agenda"]["url"]}]
        if obj.get("Agenda Packet"):
            return [{"title": "Agenda Packet", "href": obj["Agenda Packet"]["url"]}]
        if obj.get("Minutes"):
            return [{"title": "Minutes", "href": obj["Minutes"]["url"]}]
        if obj.get("Video"):
            return [{"title": "Video", "href": obj["Video"]["url"]}]
        

