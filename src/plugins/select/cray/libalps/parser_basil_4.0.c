/*
 * XML tag handlers specific to Basil 4.0 (development release)
 *
 * Copyright (c) 2009-2011 Centro Svizzero di Calcolo Scientifico (CSCS)
 * Licensed under the GPLv2.
 */
#include "parser_internal.h"

/** Basil 4.0 'Released' element */
static void eh_released_4_0(struct ud *ud, const XML_Char **attrs)
{
	char *attribs[] = { "claims" };
	/*
	 * The 'claims' attribute is new in Basil 4.0 and indicates the
	 * number of claims still outstanding against the reservation.
	 * If the 'claims' value is 0, the reservation is assured to have
	 * been removed.
	 */
	eh_released_3_1(ud, attrs);
	extract_attributes(attrs, attribs, ARRAY_SIZE(attribs));

	if (atou32(attribs[0], &ud->bp->mdata.res->claims) < 0)
		fatal("illegal claims = %s", attribs[0]);
}

/** Basil 4.0 'NodeArray' element */
static void eh_node_array_4_0(struct ud *ud, const XML_Char **attrs)
{
	char *attribs[] = { "changecount" };
	/*
	 * The 'changecount' attribute is new in Basil 4.0. Quoting Basil 1.2
	 * documentation:
	 * "A new attribute to the NodeArray element in both QUERY(INVENTORY)
	 *  method requests and responses, changecount, is used to associate a
	 *  single value (the number of changes to the set of data since
	 *  initialization) with all values found in node data (exempting
	 *  resource allocation data). In a QUERY(INVENTORY) method response
	 *  that includes node data, the value of the changecount attribute of
	 *  the NodeArray element is monotonically increasing, starting at '1'.
	 *
	 *  Each time any data contained within the NodeArray element changes
	 *  (again, exempting resource allocation data like memory allocations,
	 *  processor allocations, or accelerator allocations), the value of the
	 *  changecount attribute is incremented. If a node's state transitions
	 *  from up to down, the value will be incremented. If that same node's
	 *  state again transitions, this time from down to up, the value will
	 *  again be incremented, and thus be different from the original value,
	 *  even though the starting and final data is identical.
	 *
	 *  In other words, it is possible for the node data sections of two
	 *  QUERY(INVENTORY) method responses to be identical except for the
	 *  value of the changecount attribute in each of the NodeArray elements.
	 */
	extract_attributes(attrs, attribs, ARRAY_SIZE(attribs));

	if (atou64(attribs[0], &ud->bp->mdata.inv->change_count) < 0)
		fatal("illegal change_count = %s", attribs[0]);
}

const struct element_handler basil_4_0_elements[] = {
	[BT_MESSAGE]	= {
			.tag	= "Message",
			.depth	= 0xff,	/* unused, can appear at any depth */
			.uniq	= false,
			.hnd	= eh_message
	},
	[BT_RESPONSE]	= {
			.tag	= "BasilResponse",
			.depth	= 0,
			.uniq	= true,
			.hnd	= eh_response
	},
	[BT_RESPDATA]	= {
			.tag	= "ResponseData",
			.depth	= 1,
			.uniq	= true,
			.hnd	= eh_resp_data
	},
	[BT_RESERVED]	= {
			.tag	= "Reserved",
			.depth	= 2,
			.uniq	= true,
			.hnd	= eh_reserved
	},
	[BT_RESVDNODEARRAY] = {
			.tag	= "ReservedNodeArray",
			.depth	= 3,
			.uniq	= true,
			.hnd	= NULL
	},
	[BT_RESVDNODE] = {
			.tag	= "ReservedNode",
			.depth	= 4,
			.uniq	= false,
			.hnd	= eh_resvd_node
	},
	[BT_CONFIRMED]	= {
			.tag	= "Confirmed",
			.depth	= 2,
			.uniq	= true,
			.hnd	= eh_confirmed
	},
	[BT_RELEASED]	= {
			.tag	= "Released",
			.depth	= 2,
			.uniq	= true,
			.hnd	= eh_released_4_0
	},
	[BT_ENGINE]	= {
			.tag	= "Engine",
			.depth	= 2,
			.uniq	= true,
			.hnd	= eh_engine_3_1
	},
	[BT_INVENTORY]	= {
			.tag	= "Inventory",
			.depth	= 2,
			.uniq	= true,
			.hnd	= eh_inventory_3_1
	},
	[BT_NODEARRAY]	= {
			.tag	= "NodeArray",
			.depth	= 3,
			.uniq	= true,
			.hnd	= eh_node_array_4_0
	},
	[BT_NODE]	= {
			.tag	= "Node",
			.depth	= 4,
			.uniq	= false,
			.hnd	= eh_node_3_1
	},
	[BT_SEGMARRAY]	= {
			.tag	= "SegmentArray",
			.depth	= 5,
			.uniq	= true,
			.hnd	= NULL
	},
	[BT_SEGMENT]	= {
			.tag	= "Segment",
			.depth	= 6,
			.uniq	= false,
			.hnd	= eh_segment
	},
	[BT_PROCARRAY]	= {
			.tag	= "ProcessorArray",
			.depth	= 7,
			.uniq	= true,
			.hnd	= NULL
	},
	[BT_PROCESSOR]	= {
			.tag	= "Processor",
			.depth	= 8,
			.uniq	= false,
			.hnd	= eh_proc
	},
	[BT_PROCALLOC]	= {
			.tag	= "ProcessorAllocation",
			.depth	= 9,
			.uniq	= false,
			.hnd	= eh_proc_alloc
	},
	[BT_MEMARRAY]	= {
			.tag	= "MemoryArray",
			.depth	= 7,
			.uniq	= true,
			.hnd	= NULL
	},
	[BT_MEMORY]	= {
			.tag	= "Memory",
			.depth	= 8,
			.uniq	= false,
			.hnd	= eh_mem
	},
	[BT_MEMALLOC]	= {
			.tag	= "MemoryAllocation",
			.depth	= 9,
			.uniq	= false,
			.hnd	= eh_mem_alloc
	},
	[BT_LABELARRAY]	= {
			.tag	= "LabelArray",
			.depth	= 7,
			.uniq	= true,
			.hnd	= NULL
	},
	[BT_LABEL]	= {
			.tag	= "Label",
			.depth	= 8,
			.uniq	= false,
			.hnd	= eh_label
	},
	[BT_RESARRAY]	= {
			.tag	= "ReservationArray",
			.depth	= 3,
			.uniq	= true,
			.hnd	= NULL
	},
	[BT_RESVN]	= {
			.tag	= "Reservation",
			.depth	= 4,
			.uniq	= false,
			.hnd	= eh_resv_3_1
	},
	[BT_APPARRAY]	= {
			.tag	= "ApplicationArray",
			.depth	= 5,
			.uniq	= true,
			.hnd	= NULL
	},
	[BT_APPLICATION]	= {
			.tag	= "Application",
			.depth	= 6,
			.uniq	= false,
			.hnd	= eh_application
	},
	[BT_CMDARRAY]	= {
			.tag	= "CommandArray",
			.depth	= 7,
			.uniq	= true,
			.hnd	= NULL
	},
	[BT_COMMAND]	= {
			.tag	= "Command",
			.depth	= 8,
			.uniq	= false,
			.hnd	= eh_command
	},
	[BT_4_0_MAX]	= {
			NULL, 0, 0, NULL
	}
};
