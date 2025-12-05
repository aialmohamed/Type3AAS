"""
PubSub utility class for extended XMPP PubSub operations.
Provides owner-level operations not available in spade_pubsub.
"""

from typing import Optional
from slixmpp.plugins.xep_0060 import XEP_0060


class PubSubOwnerUtils:
    """
    Utility class for PubSub owner-level operations.
    Wraps the XEP-0060 plugin to provide easy access to owner queries.
    """

    def __init__(self, client, pubsub_service: str = "pubsub.localhost"):
        """
        Initialize the PubSub utility.

        Args:
            client: The SPADE agent's XMPP client (self.client)
            pubsub_service: The PubSub service JID (default: pubsub.localhost)
        """
        self.client = client
        self.pubsub_service = pubsub_service
        self.xep_0060: XEP_0060 = client["xep_0060"]

    async def get_node_subscribers(self, node: str) -> list[str]:
        """
        Get all subscribers to a node (owner-only).

        Args:
            node: The node name to query

        Returns:
            List of JIDs subscribed to the node
        """
        try:
            result = await self.xep_0060.get_node_subscriptions(
                self.pubsub_service, node
            )
            subscribers = []
            if result["pubsub_owner"] and result["pubsub_owner"]["subscriptions"]:
                for sub in result["pubsub_owner"]["subscriptions"]:
                    if sub["subscription"] == "subscribed":
                        subscribers.append(str(sub["jid"]))
            return subscribers
        except Exception as e:
            print(f"Error getting node subscribers: {e}")
            return []

    async def get_node_affiliations(self, node: str) -> dict[str, str]:
        """
        Get all affiliations for a node (owner-only).

        Args:
            node: The node name to query

        Returns:
            Dict mapping JID to affiliation (owner, publisher, member, outcast, none)
        """
        try:
            result = await self.xep_0060.get_node_affiliations(
                self.pubsub_service, node
            )
            affiliations = {}
            if result["pubsub_owner"] and result["pubsub_owner"]["affiliations"]:
                for aff in result["pubsub_owner"]["affiliations"]:
                    affiliations[str(aff["jid"])] = aff["affiliation"]
            return affiliations
        except Exception as e:
            print(f"Error getting node affiliations: {e}")
            return {}

    async def set_affiliation(self, node: str, jid: str, affiliation: str) -> bool:
        """
        Set affiliation for a JID on a node (owner-only).

        Args:
            node: The node name
            jid: The JID to set affiliation for
            affiliation: One of 'owner', 'publisher', 'member', 'outcast', 'none'

        Returns:
            True if successful, False otherwise
        """
        valid_affiliations = {"owner", "publisher", "member", "outcast", "none"}
        if affiliation not in valid_affiliations:
            print(f"Invalid affiliation: {affiliation}. Must be one of {valid_affiliations}")
            return False

        try:
            await self.xep_0060.modify_affiliations(
                self.pubsub_service,
                node,
                [(jid, affiliation)]
            )
            print(f"Set {jid} as {affiliation} on {node}")
            return True
        except Exception as e:
            print(f"Error setting affiliation: {e}")
            return False

    async def set_subscription(self, node: str, jid: str, subscription: str) -> bool:
        """
        Modify subscription state for a JID on a node (owner-only).

        Args:
            node: The node name
            jid: The JID to modify subscription for
            subscription: One of 'subscribed', 'pending', 'unconfigured', 'none'

        Returns:
            True if successful, False otherwise
        """
        valid_subscriptions = {"subscribed", "pending", "unconfigured", "none"}
        if subscription not in valid_subscriptions:
            print(f"Invalid subscription: {subscription}. Must be one of {valid_subscriptions}")
            return False

        try:
            await self.xep_0060.modify_subscriptions(
                self.pubsub_service,
                node,
                [(jid, subscription)]
            )
            print(f"Set {jid} subscription to {subscription} on {node}")
            return True
        except Exception as e:
            print(f"Error setting subscription: {e}")
            return False

    async def get_node_config(self, node: str) -> Optional[dict]:
        """
        Get node configuration (owner-only).

        Args:
            node: The node name

        Returns:
            Dict of configuration options or None on error
        """
        try:
            result = await self.xep_0060.get_node_config(self.pubsub_service, node)
            if result["pubsub_owner"] and result["pubsub_owner"]["configure"]:
                form = result["pubsub_owner"]["configure"]["form"]
                return {field["var"]: field["value"] for field in form["fields"]}
            return {}
        except Exception as e:
            print(f"Error getting node config: {e}")
            return None

    async def delete_node(self, node: str) -> bool:
        """
        Delete a node (owner-only).

        Args:
            node: The node name to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            await self.xep_0060.delete_node(self.pubsub_service, node)
            print(f"Deleted node {node}")
            return True
        except Exception as e:
            print(f"Error deleting node: {e}")
            return False

    async def purge_node(self, node: str) -> bool:
        """
        Purge all items from a node (owner-only).

        Args:
            node: The node name to purge

        Returns:
            True if successful, False otherwise
        """
        try:
            await self.xep_0060.purge(self.pubsub_service, node)
            print(f"Purged node {node}")
            return True
        except Exception as e:
            print(f"Error purging node: {e}")
            return False